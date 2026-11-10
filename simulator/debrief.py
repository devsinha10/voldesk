"""Daily takeaways, end-of-session scorecard and the (Claude or rule-based) review."""
from __future__ import annotations

from typing import Optional

import numpy as np

from grading.llm import api_available, session_review


def _f(x: float) -> str:
    return f"{x:+,.0f}"


def day_takeaway(d: dict, sess) -> str:
    """One-line, rule-based takeaway from a day's P&L breakdown (USD)."""
    greek = {k: d[k] for k in ("delta", "gamma", "vega", "theta", "vanna", "volga")}
    main = max(greek, key=lambda k: abs(greek[k]))
    gt = d["gamma"] + d["theta"]
    if abs(d["delta"]) > 0.5 * (abs(d["gamma"]) + abs(d["vega"]) + abs(d["theta"]) + 1):
        return (f"Delta drove the day ({_f(d['delta'])} USD): you carried open spot risk. Hedge sooner after client "
                f"trades and before events.")
    if main == "vega":
        b = max(d["vega_by_tenor"], key=lambda k: abs(d["vega_by_tenor"][k])) if d["vega_by_tenor"] else "n/a"
        return f"Vega dominated ({_f(d['vega'])} USD, mostly {b}): your vol position, not spot, made the day."
    if main in ("gamma", "theta"):
        verdict = "realised beat implied (long gamma paid)" if gt > 0 and d["gamma"] > 0 else \
                  "implied beat realised (short gamma paid)" if gt > 0 else "the gamma/theta trade went against you"
        return f"Gamma {_f(d['gamma'])} vs theta {_f(d['theta'])}: {verdict}."
    if d["edge"] > 0 and d["edge"] > abs(d["hedge_cost"]) * 2:
        return f"Client edge {_f(d['edge'])} covered hedging costs {_f(d['hedge_cost'])}: good franchise day."
    return f"Largest Greek P&L came from {main} ({_f(greek[main])} USD)."


def scorecard(sess) -> dict:
    t = sess.total_terms
    c = sess.counters
    market = sum(t[k] for k in ("delta", "gamma", "vega", "theta", "vanna", "volga", "rho"))
    quoted = max(c["quoted"], 1)
    inf = sess.informed_pnl()
    return {
        "total_pnl_usd": sess.pnl_usd,
        "penalty_usd": sess.penalty_usd,
        "score_usd": sess.pnl_usd - sess.penalty_usd,
        "edge_captured_usd": t["edge"],
        "hedging_costs_usd": t["hedge_cost"],
        "carry_usd": t["carry"],
        "market_pnl_usd": market,
        "realised_vol_luck_usd (gamma+theta)": t["gamma"] + t["theta"],
        "vol_moves_usd (vega+vanna+volga)": t["vega"] + t["vanna"] + t["volga"],
        "delta_pnl_usd": t["delta"],
        "unexplained_usd": t["unexplained"],
        "hedge_cost_as_pct_of_edge": (abs(t["hedge_cost"]) / t["edge"] * 100) if t["edge"] > 0 else None,
        "avg_delta_limit_used_pct": float(np.mean(sess.delta_util) * 100) if sess.delta_util else 0.0,
        "limit_breach_ticks": dict(sess.breach_ticks),
        "rfqs": c["rfqs"], "quoted": c["quoted"], "traded": c["traded"], "passed": c["passed"], "missed": c["missed"],
        "fill_rate_pct": c["traded"] / quoted * 100,
        "pnl_on_informed_client_trades_usd": inf,
        "vega_by_tenor_usd": dict(t["vega_by_tenor"]),
        "regime": sess.market.regime, "level": sess.level, "seed": sess.seed, "pairs": sess.pairs,
    }


def rule_based_review(sess, card: dict) -> str:
    """Fallback review (no API key): the three biggest logged decisions."""
    items = []
    if sess.trades:
        best = max(sess.trades, key=lambda x: x["edge_usd"])
        items.append(f"Best-priced trade: {best['desc']} at {best['price']:.2f} vs fair {best['fair']:.2f} "
                     f"(edge {best['edge_usd']:,.0f} USD, client {best['client']}). Keep quoting with that discipline.")
        inf = [x for x in sess.trades if x["informed"] or x["client"] == "macro_hf"]
        if inf:
            w = inf[0]
            items.append(f"Trade with an informed client: {w['desc']} on day {int(w['t']) + 1}. Informed flow moved "
                         f"the market their way; P&L on informed-client trades {card['pnl_on_informed_client_trades_usd']:,.0f} "
                         f"USD. Widen and skew quotes for fast money, and hedge quickly after trading with them.")
    if card["limit_breach_ticks"]:
        k = max(card["limit_breach_ticks"], key=card["limit_breach_ticks"].get)
        items.append(f"Limit breaches: {k} was over its limit for {card['limit_breach_ticks'][k]} ticks "
                     f"(total penalty {card['penalty_usd']:,.0f} USD). Hedge back inside limits immediately.")
    if abs(card["delta_pnl_usd"]) > abs(card["edge_captured_usd"]):
        items.append(f"Delta P&L of {card['delta_pnl_usd']:,.0f} USD outweighed your edge of "
                     f"{card['edge_captured_usd']:,.0f} USD: the session was decided by spot risk you did not need.")
    if card["missed"]:
        items.append(f"You missed {card['missed']} RFQs: a quick wide price beats no price.")
    items = items[:3] or ["Quiet session: not enough logged decisions to review."]
    return "\n".join(f"{i + 1}. {x}" for i, x in enumerate(items))


def compact_log(sess, max_events: int = 400) -> list[dict]:
    """Event log trimmed for the review prompt (drops routine RFQ arrivals if long)."""
    log = sess.log
    if len(log) <= max_events:
        return log
    keep = [e for e in log if e["kind"] != "rfq"]
    return keep[-max_events:]


def claude_review(sess, card: dict) -> Optional[str]:
    if not api_available():
        return None
    return session_review(compact_log(sess), card)

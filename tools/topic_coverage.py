"""python -m tools.topic_coverage  ->  audit/topic_coverage.md

Every topic from the original spec, the level(s) where generated questions now
cover it (found by sampling the generators), and a flag for anything missing.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from tools.common import sample

OUT = Path(__file__).resolve().parent.parent / "audit" / "topic_coverage.md"


def T(*names):
    """Template equals a name, or starts with a name ending in '*'."""
    exact = {n for n in names if not n.endswith("*")}
    prefixes = tuple(n[:-1] for n in names if n.endswith("*"))
    return lambda q: q.template in exact or (bool(prefixes) and q.template.startswith(prefixes))


def TOPIC(*names):
    return lambda q: q.topic in names


def TAG(tag, sub=None):
    return lambda q: (sub is None or q.subsection == sub) and any(tag in str(x) for x in q.tags)


def TEXT(s, sub=None):
    return lambda q: (sub is None or q.subsection == sub) and s.lower() in (q.prompt + q.model_answer).lower()


def ANY(*fs):
    return lambda q: any(f(q) for f in fs)


SPEC = [
    # ---- Section 1 ----
    ("1A", "Delta, gamma, theta, vega, rho: direction after spot/vol/time changes", T("matrix_L1")),
    ("1A", "Which has more gamma/vega/theta (e.g. 1W vs 3M ATM)", T("compare")),
    ("1A", "Vanna, volga, charm (+ speed, veta) direction", T("matrix_L2")),
    ("1A", "First-order Greek moves explained via a second-order Greek", T("via_second_order")),
    ("1A", "Vega sqrt(T) scaling after time passes", T("time_scaling")),
    ("1A", "Vega by tenor bucket (why not just +200k)", T("vega_buckets")),
    ("1A", "Delta-hedged P&L ~ 0.5 Gamma S^2 (realised var - implied var)", T("rv_iv")),
    ("1A", "Breakeven daily move for theta", T("breakeven")),
    ("1B", "Long/short calls and puts", ANY(TOPIC("exposures:call"), TOPIC("exposures:put"))),
    ("1B", "Straddle", TOPIC("exposures:straddle")),
    ("1B", "Strangle", TOPIC("exposures:strangle")),
    ("1B", "Risk reversal", TOPIC("exposures:risk_reversal")),
    ("1B", "Call/put spreads", ANY(TOPIC("exposures:call_spread"), TOPIC("exposures:put_spread"))),
    ("1B", "Butterfly", TOPIC("exposures:butterfly")),
    ("1B", "Calendar", TOPIC("exposures:calendar")),
    ("1B", "Collar", TOPIC("exposures:collar")),
    ("1B", "Ratio spread", TOPIC("exposures:ratio_spread")),
    ("1B", "Delta-hedged versions", TEXT("delta-hedged", "1B")),
    ("1B", "Equity index for variety", TAG("equity", "1B")),
    ("1B", "Shock: IV spike / crush", ANY(TAG("iv_spike", "1B"), TAG("iv_crush", "1B"))),
    ("1B", "Shock: spot rally / selloff", ANY(TAG("spot_rally", "1B"), TAG("spot_selloff", "1B"))),
    ("1B", "Shock: time passing / approaching expiry", ANY(TAG("time_passes", "1B"), TAG("approaching_expiry", "1B"))),
    ("1B", "Shock: skew steepening", TAG("skew_steepen", "1B")),
    ("1B", "Shock: term structure inverting", TAG("term_invert", "1B")),
    ("1B", "Vanna/volga/charm in the sign table", lambda q: q.subsection == "1B" and q.parts and "Vanna" in getattr(q.parts[0], "rows", [])),
    ("1B", "P&L estimate from Greeks (Givens)", lambda q: q.subsection == "1B" and bool(q.givens)),
    ("1C", "Put-call parity", T("arb_calc_parity")),
    ("1C", "Spread bounds (call spread at 11)", T("arb_call_spread", "arb_put_spread", "arb_calc_call_spread")),
    ("1C", "Butterfly arbitrage", T("arb_butterfly", "arb_calc_butterfly")),
    ("1C", "Calendar arbitrage", T("arb_calendar", "arb_calc_calendar")),
    ("1C", "Implied vs realised vol", T("rv_iv")),
    ("1C", "Gamma-theta trade-off / breakeven", T("breakeven")),
    ("1C", "Explaining P&L outcomes with Greeks", T("puzzle*")),
    ("1C", "Why skew exists (equity vs USDJPY vs other FX)", T("skew")),
    ("1C", "Skew dynamics with numbers", T("skew_pnl")),
    ("1C", "Sticky strike vs sticky delta", T("sticky_calc")),
    ("1C", "Choosing the right structure for a view", T("view_match", "trade_vol_up", "trade_overpriced")),
    ("1C", "Event expiry choice (e.g. BoJ meeting)", T("trade_vol_up", "trade_overpriced")),
    # ---- Section 2 ----
    ("2A-1", "Long vs short a bond; gain/lose", T("s1_l1_position")),
    ("2A-1", "Zero vs coupon; short vs long maturity; coupon effect", T("s1_l1_compare")),
    ("2A-1", "Positive convexity; big moves either way", T("s1_l1_asymmetry", "s1_l2_asym_sized")),
    ("2A-1", "Sized P&L with D_mod and convexity given", T("s1_l2_sized")),
    ("2A-1", "Compute D_mod / DV01 from bond details", T("s1_l3_compute")),
    ("2A-1", "Approximation vs full repricing", T("s1_l3_big_move", "s1_l2_sized")),
    ("2A-2", "Long a future = long duration", T("s2_l1_futures", "s2_l2_fut_pnl")),
    ("2A-2", "Repo funding and carry", T("s2_l1_repo", "s2_l2_carry")),
    ("2A-2", "Futures hedge ratio (CTD DV01 / CF)", T("s2_l3_hedge")),
    ("2A-3", "Receive fixed = long duration; pay = short", T("s3_l1_swap", "s3_l2_swap_pnl")),
    ("2A-3", "Floater has almost no duration", T("s3_l1_floater")),
    ("2A-3", "Forward-starting swaps", T("s3_l1_forward", "s3_l3_annuity")),
    ("2A-4", "Receiver/payer swaption duration and convexity; short = short convexity", T("s4_l1_signs")),
    ("2A-4", "Swaption duration changes as rates move", T("s4_l2_delta")),
    ("2A-4", "Bachelier swaption pricing and DV01", T("s4_l3_bachelier")),
    ("2A-5", "Mixed books (receive 10Y + long payers, etc.)", T("s5_l1_signs", "s5_l2_move", "s5_l3_taylor")),
    ("2A-5", "Callable bonds / MBS: long duration, short convexity",
     lambda q: q.subsection == "2A-5" and q.facts.get("variant") in ("callable", "mbs_hedged")),
    ("2B", "Long convexity gains from big moves and costs carry", T("b_l1_cost", "b_l3_straddle")),
    ("2B", "Convexity ~ maturity squared", T("b_l2_maturity")),
    ("2B", "Barbell vs bullet", T("b_l1_barbell", "b_l2_barbell")),
    ("2B", "Mortgage convexity hedging", T("b_l1_mbs")),
    ("2C", "Steepeners/flatteners, bull/bear", T("c_l1_label", "c_l2_pnl")),
    ("2C", "DV01-weighted legs vs equal notional", T("c_l2_sizing", "c_l3_full")),
    ("2C", "BoE cuts sooner than priced: trade and sizing", T("c_l1_boe")),
    ("2C", "Convexity of curve trades", T("c_l1_convexity_sign", "c_l1_convexity_big_move", "c_l2_convexity_pnl")),
    ("2D", "Carry and roll-down", T("d_l1_sign", "d_l2", "d_l3")),
    ("2D", "Breakeven yield moves", T("d_l1_kills", "d_l3")),
    ("2E", "Reading cuts/hikes priced into OIS", T("e_l1_read", "e_l2")),
    ("2E", "Implied meeting probabilities (15bp -> 60%)", T("e_l2", "e_l3")),
    ("2E", "Market reaction to a surprise", T("e_l1_react")),
    ("2F", "Bond futures CTD and basis", T("f_l2_ctd")),
    ("2F", "The short's delivery option", TOPIC("advanced:delivery_option")),
    ("2F", "Swap spreads and why they can go negative", TOPIC("advanced:swap_spreads")),
    ("2F", "Rates vol in normal terms", T("f_l2_nvol")),
    ("2F", "Who is structurally long/short rates vol", TOPIC("advanced:vol_owners")),
    ("2F", "Curve butterflies: PCA vs DV01 weighting", ANY(T("c_l3_fly"), TOPIC("advanced:fly"))),
    ("2F", "Key-rate DV01", T("f_l3_krd")),
    ("2F", "2022 UK gilt/LDI crisis", ANY(T("f_l3_ldi"), TOPIC("advanced:ldi_2022"))),
]


def coverage(n: int = 40) -> list[tuple[str, str, list[int]]]:
    qs = sample(n)
    out = []
    for sub, name, pred in SPEC:
        levels = sorted({lvl for (sec, code, lvl), lst in qs.items() for q in lst if pred(q)})
        out.append((sub, name, levels))
    return out


def main(n: int = 40) -> Path:
    rows = coverage(n)
    missing = [r for r in rows if not r[2]]
    lines = ["# Topic coverage against the original spec", "",
             f"Found by sampling {n} questions per sub-section per level. Levels listed are where the topic appears.", "",
             f"**Missing topics: {len(missing)}**" + ("" if not missing else ": " + "; ".join(f"{s} {t}" for s, t, _ in missing)),
             "", "| Sub-section | Topic | Levels |", "|---|---|---|"]
    lines += [f"| {s} | {t} | {', '.join(f'L{x}' for x in lv) or '**MISSING**'} |" for s, t, lv in rows]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    print(f"wrote {main()}")

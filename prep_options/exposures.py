"""Section 1B: write your Greek exposures for a structure, then explain how they
change under a shock. Signs and before/after numbers come from the engine."""
from __future__ import annotations

import numpy as np

from engine.fx_conventions import TENORS
from engine.pnl_attribution import revaluation_breakdown
from engine.structures import build, describe
from grading.question import Part, Question, chart_line
from prep_options.common import (GREEK_LABEL, GREEK_UNITS, describe_position_change, fmt_greek, fmt_num,
                                 fx_market, pick_pair, profile, spot_grid, spx_market, tenor_text)

ROW_KEYS_BASE = {"Delta": "delta", "Gamma": "gamma_1pct", "Theta": "theta", "Vega": "vega",
            "Vanna": "vanna", "Volga": "volga"}

KINDS = {
    1: ["call", "put", "straddle", "strangle"],
    2: ["call", "put", "straddle", "strangle", "risk_reversal", "call_spread", "put_spread",
        "butterfly", "collar"],
    3: ["call", "put", "straddle", "strangle", "risk_reversal", "call_spread", "put_spread",
        "butterfly", "collar", "calendar", "ratio_spread"],
}
SHOCKS = {
    1: ["iv_spike", "iv_crush", "spot_rally", "spot_selloff", "time_passes"],
    2: ["iv_spike", "iv_crush", "spot_rally", "spot_selloff", "time_passes", "approaching_expiry"],
    3: ["iv_spike", "iv_crush", "spot_rally", "spot_selloff", "time_passes", "approaching_expiry",
        "skew_steepen", "term_invert"],
}

SHOCK_MECH = {
    "iv_spike": {
        "gamma_1pct": "Higher vol spreads gamma over a wider range of spot: gamma near the strikes falls (ATM gamma ~ 1/vol) and gamma at far strikes rises.",
        "vega": "ATM vega barely moves with the vol level (volga ~ 0 ATM); wing vega rises (positive volga). Long-wing structures gain vega.",
        "theta": "ATM theta scales roughly with vol, so the daily decay (paid or received) grows.",
        "delta": "Vol up pulls every strike's delta towards 50 (vanna): OTM deltas grow, ITM deltas shrink.",
    },
    "iv_crush": {
        "gamma_1pct": "Lower vol concentrates gamma near the strikes: ATM gamma rises, far-strike gamma falls.",
        "vega": "ATM vega barely changes; wing vega falls (positive volga in the wings).",
        "theta": "Theta scales with vol, so time decay shrinks.",
        "delta": "Vol down pushes deltas away from 50: OTM deltas shrink, ITM deltas grow.",
    },
    "spot_move": {
        "gamma_1pct": "Gamma, vega and theta are concentrated near each strike: whichever strikes spot moves towards now dominate the risk.",
        "vega": "Vega peaks near each strike, so it follows spot towards (up) or away from (down) the strikes.",
        "theta": "Theta mirrors gamma: it is largest near the strikes.",
        "delta": "Delta changes by roughly gamma x dS: long gamma gets longer in a rally and shorter in a selloff; short gamma the opposite.",
    },
    "time": {
        "gamma_1pct": "As expiry approaches, gamma at strikes near spot grows (~1/sqrt(T)) while gamma at strikes away from spot (ITM or OTM) collapses.",
        "vega": "Vega falls with sqrt(T): less time left means less exposure to vol.",
        "theta": "Theta at strikes near spot grows as expiry approaches; theta of options far from the strike (ITM or OTM) fades, and deep ITM options can even earn carry.",
        "delta": "Charm: OTM deltas decay towards 0 and ITM deltas grow towards 100 as time passes.",
    },
    "skew_steepen": {
        "gamma_1pct": "A skew move changes each strike's vol differently: low-strike vols rise, high-strike vols fall, so each leg's gamma moves the opposite way to its vol.",
        "vega": "Each leg's vega responds to its own vol change via volga; wing legs are affected most.",
        "theta": "Legs whose vol rose decay faster, legs whose vol fell decay slower.",
        "delta": "Each leg's delta moves via vanna and its own vol change: puts' deltas grow in size as their vols rise.",
    },
    "term_invert": {
        "gamma_1pct": "Front-end vols up and back-end down: short-dated gamma falls, longer-dated gamma rises slightly.",
        "vega": "Vega per tenor bucket now matters: the front-end legs gained vol, the back-end legs lost vol.",
        "theta": "Front-end theta grows with the higher front vol; back-end theta shrinks.",
        "delta": "Deltas shift via vanna, in different directions for the front and back legs.",
    },
}


def _apply_shock(rng, mkt, shock: str, tau: float, legs_expiry_min: float):
    v0 = mkt.vol(mkt.forward(tau), tau)
    if shock == "iv_spike":
        pts = round(float(rng.uniform(2.0, 6.0)) * max(v0 / 0.08, 0.7), 1)
        return mkt.bump_vol(pts), f"implied vol spikes {pts:.1f} vol points across the surface", "iv_spike"
    if shock == "iv_crush":
        pts = round(float(rng.uniform(1.0, max(1.2, 0.35 * v0 * 100))), 1)
        return mkt.bump_vol(-pts), f"implied vol is crushed {pts:.1f} vol points across the surface", "iv_crush"
    if shock in ("spot_rally", "spot_selloff"):
        sd_move = v0 * np.sqrt(tau) * 100
        pct = round(float(np.clip(rng.uniform(0.6, 1.2) * sd_move, 0.8, 6.0)), 1)
        pct = pct if shock == "spot_rally" else -pct
        word = "rallies" if pct > 0 else "sells off"
        return mkt.bump_spot(pct), f"spot {word} {abs(pct):.1f}% (vol surface sticky by strike)", "spot_move"
    if shock == "time_passes":
        days = round(legs_expiry_min * 365 * 0.5)
        return mkt.pass_time(days), f"{days:.0f} days pass with spot and vols unchanged", "time"
    if shock == "approaching_expiry":
        days = max(legs_expiry_min * 365 - 2, 1)
        return mkt.pass_time(days), f"time passes until 2 days are left to the (nearest) expiry, spot and vols unchanged", "time"
    if shock == "skew_steepen":
        pts = round(float(rng.uniform(1.0, 3.0)), 1)
        return mkt.bump_skew(-pts), f"the skew steepens: 25d risk reversals move {pts:.1f} vols further towards puts", "skew_steepen"
    if shock == "term_invert":
        pts = round(float(rng.uniform(2.0, 4.0)), 1)
        return mkt.invert_term(pts), f"the term structure inverts: front-end vols rise ~{pts:.1f} pts, 1Y falls ~{pts/2:.1f} pts", "term_invert"
    raise ValueError(shock)


def generate(seed: int, difficulty: int) -> Question:
    rng = np.random.default_rng(seed)
    equity = rng.random() < 0.15
    if equity:
        mkt = spx_market()
        N = float(rng.choice([500, 1000, 2000]))
        name = mkt.name
    else:
        pair = pick_pair(rng)
        mkt = fx_market(pair)
        N = float(rng.choice([10e6, 25e6, 50e6]))
        name = pair
    kind = str(rng.choice(KINDS[difficulty]))
    side = int(rng.choice([1, -1]))
    tenor = str(rng.choice(["1M", "3M"] if difficulty == 1 else ["1W", "1M", "3M", "6M", "1Y"]))
    if kind == "calendar":
        tenor = str(rng.choice(["1W", "1M"]))
    hedged = difficulty >= 2 and kind not in ("collar", "straddle") and rng.random() < 0.35
    md = None
    if kind in ("call", "put") and difficulty >= 2 and rng.random() < 0.5:
        md = float(rng.choice([0.25, 0.75]))
    struct = build(kind, mkt, tenor, N, side=side, moneyness_delta=md, hedged=hedged)
    shock = str(rng.choice(SHOCKS[difficulty]))
    tau = TENORS[tenor]
    exp_min = min(l.expiry for l in struct.legs if l.kind == "option") - mkt.t
    m1, shock_text, mech_key = _apply_shock(rng, mkt, shock, tau, exp_min)
    rows = ["Delta", "Gamma", "Theta", "Vega"] + (["Vanna", "Volga"] if difficulty == 3 else [])
    ROW_KEYS = dict(ROW_KEYS_BASE)
    if mkt.premium_adjusted:
        ROW_KEYS["Delta"] = "delta_pa"  # market convention for this pair

    e0, e1 = struct.exposure(mkt), struct.exposure(m1)
    # reference magnitudes for "flat": a single ATM option (and a 25d option for vanna/volga)
    ref_atm = build("call", mkt, tenor, N).exposure(mkt)
    ref_25 = build("call", mkt, tenor, N, moneyness_delta=0.25).exposure(mkt)
    refs = {"delta": N, "delta_pa": N, "gamma_1pct": ref_atm.gamma_1pct, "theta": ref_atm.theta, "vega": ref_atm.vega,
            "vanna": ref_25.vanna, "volga": ref_25.volga}
    correct = {}
    for r in rows:
        k = ROW_KEYS[r]
        v, ref = getattr(e0, k), abs(refs[k])
        sgn = "0" if abs(v) < 0.10 * ref else ("+" if v > 0 else "-")
        if 0.10 * ref <= abs(v) < 0.2 * ref:
            correct[r] = [sgn, "0"]  # borderline: accept 'flat' too
        else:
            correct[r] = sgn

    desc = describe(kind, side, tenor, name, hedged, moneyness_delta=md)
    strikes = ", ".join(f"{l.label} K={l.K:.{(mkt.pair.decimals if mkt.pair else 0)}f}"
                        for l in struct.legs if l.kind == "option")
    conv = mkt.pair.convention_label(tau) if mkt.pair else "Black-Scholes, ATM = DNS"
    prompt = (f"You are **{desc}**, notional {('$' if equity else '')}{fmt_num(N).lstrip('+')}"
              f"{' units' if equity else ' ' + mkt.pair.base} per leg.\n\n"
              f"Spot {mkt.spot:,.{(mkt.pair.decimals if mkt.pair else 0)}f}. Legs: {strikes}. "
              f"Convention: {conv}.\n\n"
              f"1. Fill in the sign of each exposure **now** (+ long, - short, 0 roughly flat).\n"
              f"2. Then describe how your exposures change if **{shock_text}**, and what it does to your P&L.")

    bd = revaluation_breakdown(struct.legs, mkt, m1)
    pnl = bd.pop("total")
    terms = bd
    main = max(terms, key=lambda k: abs(terms[k]))

    # model answer
    fmtk = lambda k: (lambda v: fmt_greek(mkt, k, v))
    lines = ["**Exposures before the shock** (engine):"]
    for r in rows:
        k = ROW_KEYS[r]
        c = correct[r] if isinstance(correct[r], str) else correct[r][0]
        lines.append(f"- {r}: **{c}** ({fmt_greek(mkt, k, getattr(e0, k))}, {GREEK_UNITS[k]})")
    intuition = _structure_intuition(kind, side, hedged)
    lines += ["", f"**Intuition for the structure:** {intuition}", "",
              f"**After the shock ({shock_text}):**"]
    for r in ["Delta", "Gamma", "Theta", "Vega"] + (["Vanna", "Volga"] if difficulty == 3 else []):
        k = ROW_KEYS[r]
        lines.append("- " + describe_position_change(r.lower(), getattr(e0, k), getattr(e1, k), fmtk(k)) +
                     (f". {SHOCK_MECH[mech_key][k.replace('_pa', '')]}" if k.replace('_pa', '') in SHOCK_MECH[mech_key] else ""))
    lines += ["", f"**P&L from the shock:** {fmt_num(pnl)} {mkt.pair.quote if mkt.pair else 'USD'} by full revaluation. "
              f"Breakdown (spot, then vol, then time): delta {fmt_num(terms['delta'])}, gamma and higher-order "
              f"spot {fmt_num(terms['gamma'])}, vega/vol {fmt_num(terms['vega'])}, theta {fmt_num(terms['theta'])}. "
              f"The biggest driver is **{main}**."]
    refs["_pa"] = mkt.premium_adjusted
    lines += ["", "**Where the risk sits now:** " + _risk_now(e1, refs)]
    model = "\n".join(lines)

    facts = {
        "structure": desc, "notional_per_leg": N, "underlying": name, "spot": mkt.spot,
        "legs": [{"type": l.kind, "cp": l.cp, "K": l.K, "notional": l.notional, "label": l.label} for l in struct.legs],
        "shock": shock_text,
        "before": {r: getattr(e0, ROW_KEYS[r]) for r in ["Delta", "Gamma", "Theta", "Vega", "Vanna", "Volga"]},
        "after": {r: getattr(e1, ROW_KEYS[r]) for r in ["Delta", "Gamma", "Theta", "Vega", "Vanna", "Volga"]},
        "units": {r: GREEK_UNITS[ROW_KEYS[r]] for r in ROW_KEYS},
        "delta_convention": "premium-adjusted" if mkt.premium_adjusted else "unadjusted spot delta",
        "correct_signs_before": correct, "shock_pnl_total": pnl, "shock_pnl_breakdown": terms,
        "largest_pnl_driver": main,
    }
    rubric = [f"Before-shock signs: " + ", ".join(f"{r} {correct[r] if isinstance(correct[r], str) else correct[r][0]}" for r in rows),
              f"P&L from the shock is {'positive' if pnl > 0 else 'negative'}, driven mainly by {main}",
              "Gamma change: " + describe_position_change("gamma", e0.gamma_1pct, e1.gamma_1pct, fmtk("gamma_1pct")),
              "Vega change: " + describe_position_change("vega", e0.vega, e1.vega, fmtk("vega")),
              "Theta change: " + describe_position_change("theta", e0.theta, e1.theta, fmtk("theta")),
              "Delta change: " + describe_position_change("delta", getattr(e0, ROW_KEYS["Delta"]), getattr(e1, ROW_KEYS["Delta"]), fmtk(ROW_KEYS["Delta"])),
              "Mechanism for the shock: " + SHOCK_MECH[mech_key]["gamma_1pct"]]

    spots = spot_grid(mkt, exp_min if exp_min > 0 else tau)
    m1_curve = m1 if mech_key != "spot_move" else mkt
    charts = [
        chart_line("Position value vs spot", spots,
                   {"Before shock": profile(struct, mkt, "value", spots),
                    "After shock": profile(struct, m1_curve, "value", spots)},
                   "Spot", f"Value ({mkt.pair.quote if mkt.pair else 'USD'})", vline=m1.spot, vline_label="spot after"),
        chart_line("Gamma vs spot", spots,
                   {"Before shock": profile(struct, mkt, "gamma_1pct", spots),
                    "After shock": profile(struct, m1_curve, "gamma_1pct", spots)},
                   "Spot", "Gamma (delta per 1%)", vline=m1.spot, vline_label="spot after"),
        chart_line("Vega vs spot", spots,
                   {"Before shock": profile(struct, mkt, "vega", spots),
                    "After shock": profile(struct, m1_curve, "vega", spots)},
                   "Spot", "Vega (per vol pt)", vline=m1.spot, vline_label="spot after"),
    ]
    table = {"title": "Exposures before and after (engine)", "columns": ["Greek", "Units", "Before", "After"],
             "rows": [[r, GREEK_UNITS[ROW_KEYS[r]], fmt_greek(mkt, ROW_KEYS[r], getattr(e0, ROW_KEYS[r])),
                       fmt_greek(mkt, ROW_KEYS[r], getattr(e1, ROW_KEYS[r]))]
                      for r in ["Delta", "Gamma", "Theta", "Vega", "Vanna", "Volga"]]}
    return Question(section="options", subsection="1B", topic=f"exposures:{kind}", difficulty=difficulty,
                    template="exposures", seed=seed, prompt=prompt,
                    parts=[Part("sign_table", "Exposure signs before the shock", rows=rows, correct=correct, weight=1.0)],
                    free_text_prompt=f"How do your exposures change if {shock_text}? What happens to your P&L, and why?",
                    facts=facts, model_answer=model, rubric=rubric, charts=charts, tables=[table],
                    tags=[kind, shock, "equity" if equity else "fx"])


def _structure_intuition(kind: str, side: int, hedged: bool) -> str:
    s = side
    base = {
        "call": "A vanilla is long gamma, long vega and pays theta when bought; delta is positive for a call.",
        "put": "A vanilla is long gamma, long vega and pays theta when bought; delta is negative for a put.",
        "straddle": "ATM call + ATM put: delta-neutral at the DNS strike, maximum gamma and vega for the premium, and the biggest theta bill.",
        "strangle": "OTM call + OTM put: roughly delta-neutral, long gamma and vega but less than a straddle, cheaper theta; most of its volga sits in the wings.",
        "risk_reversal": "Long OTM call, short OTM put: a directional, skew trade. Delta is long, gamma and vega roughly cancel, and vanna is strongly positive (you are long the call wing's vol versus the put wing's).",
        "call_spread": "Long ATM call, short OTM call: long delta with capped upside. Net long gamma/vega near the lower strike, flipping to short near the upper strike.",
        "put_spread": "Long ATM put, short OTM put: short delta with capped payout. Net long gamma/vega near the upper strike, short near the lower strike.",
        "butterfly": "Long the wings, short 2x the body: you are short gamma and vega near the body strike and collect theta; you want spot to pin near the body.",
        "calendar": "Short the near expiry, long the far expiry at the same strike: short gamma (the near leg dominates gamma), long vega (the far leg dominates vega), and you earn theta.",
        "collar": "Long spot, long put, short call: a hedged long position. Delta stays positive (spot leg minus option deltas), gamma and vega are modest and depend on which strike spot is nearer.",
        "ratio_spread": "Long 1 ATM call, short 2 OTM calls: near the ATM strike you are long gamma, but the extra short OTM calls make you short vega and short gamma as spot rallies towards them.",
    }[kind]
    if s < 0:
        base += " You are SHORT the structure, so flip every sign."
    if hedged:
        base += " The spot hedge sets delta to zero but leaves every other Greek unchanged."
    return base


def _risk_now(e, refs) -> str:
    items = []
    for k, label in (("gamma_1pct", "gamma"), ("vega", "vega"), ("delta", "delta")):
        if k == "delta" and refs.get("_pa"):
            k = "delta_pa"
        r = getattr(e, k) / abs(refs[k]) if refs[k] else 0
        if abs(r) > 0.15:
            size = f"{abs(r)*100:.0f}% of notional" if k == "delta" else f"~{abs(r):.1f}x a single ATM option"
            items.append(f"{'long' if r > 0 else 'short'} {label} ({size})")
    return ("; ".join(items) + ".") if items else "the position is close to flat on the main Greeks."

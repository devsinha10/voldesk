"""Section 1A: quickfire Greek drills. Ground truth by bumping the engine."""
from __future__ import annotations

import numpy as np

from engine.fx_conventions import TENORS
from engine.structures import build, flat_market
from grading.question import Part, Question, chart_bar, chart_line
from prep_options.common import (GREEK_LABEL, GREEK_UNITS, direction_word, fmt_greek, fx_market,
                                 pick_pair, profile, spot_grid, tenor_text)

DIR_OPTIONS = ["Increases (in size)", "Decreases (in size)", "Roughly unchanged"]
DIR_MAP = {"Increases": 0, "Decreases": 1, "Unchanged": 2}

MONEYNESS = {  # label -> (abs delta of strike or None for ATM, itm flag)
    "ATM": None, "25-delta OTM": 0.25, "10-delta OTM": 0.10, "75-delta ITM": 0.75,
}

# Mechanism text: always-true statements about how a Greek responds to a shock.
MECH = {
    ("delta", "vol_up"): "Higher vol widens the distribution of spot at expiry, so every option looks 'more at-the-money': OTM deltas move up towards 50, ITM deltas move down towards 50 (that sensitivity is vanna).",
    ("delta", "vol_down"): "Lower vol narrows the distribution, so options look more decisively ITM or OTM: OTM deltas shrink towards 0 and ITM deltas grow towards 100.",
    ("delta", "spot_up"): "Delta changes by roughly gamma x dS. Gamma is positive for a long call or put, so a rally pushes a call's delta up and a put's delta towards 0.",
    ("delta", "spot_down"): "Delta changes by roughly gamma x dS. A selloff lowers a call's delta and pushes a put's delta towards -1.",
    ("delta", "time"): "As time passes the option has less time to change moneyness: OTM deltas decay towards 0 and ITM deltas move towards 100 (that is charm). ATM deltas stay near 50.",
    ("gamma_1pct", "vol_up"): "Gamma lives within roughly one standard deviation of the strike. Higher vol spreads it out: ATM gamma falls (it scales like 1/(vol x sqrt(T))), while far OTM gamma can rise because the strike is now fewer standard deviations away.",
    ("gamma_1pct", "vol_down"): "Lower vol concentrates gamma near the strike: ATM gamma rises and far OTM gamma falls.",
    ("gamma_1pct", "spot_up"): "Gamma peaks near the strike. Spot moving towards the strike raises it; moving away lowers it.",
    ("gamma_1pct", "spot_down"): "Gamma peaks near the strike. Spot moving towards the strike raises it; moving away lowers it.",
    ("gamma_1pct", "time"): "ATM gamma scales like 1/sqrt(T), so it grows as expiry approaches. OTM gamma eventually collapses because the strike becomes too many standard deviations away.",
    ("vega", "vol_up"): "ATM vega is almost insensitive to the vol level (volga is close to 0 at the money). OTM and ITM vega rise with vol (positive volga) because a higher vol makes the wing strikes 'closer'.",
    ("vega", "vol_down"): "ATM vega barely changes; OTM and ITM vega fall as vol falls (positive volga in the wings).",
    ("vega", "spot_up"): "Vega peaks near the strike, so it rises if spot moves towards the strike and falls if it moves away.",
    ("vega", "spot_down"): "Vega peaks near the strike, so it rises if spot moves towards the strike and falls if it moves away.",
    ("vega", "time"): "Vega scales with sqrt(T) at the money: less time left, less exposure to vol. OTM vega falls faster still.",
    ("theta", "vol_up"): "ATM theta scales with vol: theta is roughly -0.5 x gamma x S^2 x vol^2, and gamma ~ 1/vol, so the decay is ~ vol. More vol, faster decay.",
    ("theta", "vol_down"): "ATM theta scales with vol, so lower vol means slower decay.",
    ("theta", "spot_up"): "Theta is largest near the strike (it mirrors gamma), so it grows if spot moves towards the strike.",
    ("theta", "spot_down"): "Theta is largest near the strike (it mirrors gamma), so it grows if spot moves towards the strike.",
    ("theta", "time"): "ATM theta grows like 1/sqrt(T) as expiry approaches. Far OTM theta eventually falls because there is little value left to lose.",
}


def _shock(rng, mkt, kind: str, tau: float, difficulty: int):
    v0 = mkt.vol(mkt.forward(tau), tau)
    if kind == "vol_up":
        new = v0 * (2.0 if difficulty == 1 else rng.uniform(1.3, 2.0))
        pts = (new - v0) * 100
        return mkt.bump_vol(pts), f"implied vol rises from {v0*100:.1f}% to {new*100:.1f}% (all strikes)"
    if kind == "vol_down":
        new = v0 * (0.5 if difficulty == 1 else rng.uniform(0.5, 0.75))
        pts = (new - v0) * 100
        return mkt.bump_vol(pts), f"implied vol falls from {v0*100:.1f}% to {new*100:.1f}% (all strikes)"
    if kind in ("spot_up", "spot_down"):
        pct = round(float(rng.uniform(1.0, 3.0)), 1) * (1 if kind == "spot_up" else -1)
        return mkt.bump_spot(pct), f"spot {'rallies' if pct > 0 else 'sells off'} {abs(pct):.1f}% (sticky strike)"
    if kind == "time":
        frac = 0.5 if difficulty == 1 else float(rng.choice([0.5, 0.75, 0.9]))
        days = tau * 365 * frac
        return mkt.pass_time(days), f"{days:.0f} days pass with spot and vol unchanged"
    raise ValueError(kind)


def q_direction(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    """Predict the direction of a Greek after a shock (single vanilla)."""
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    greeks = ["delta", "gamma_1pct", "vega"] + (["theta"] if difficulty >= 2 else [])
    g = str(rng.choice(greeks))
    mons = ["ATM", "25-delta OTM"] + (["10-delta OTM", "75-delta ITM"] if difficulty >= 2 else [])
    mon = str(rng.choice(mons))
    cp = str(rng.choice(["C", "P"]))
    tenor = str(rng.choice(["1W", "1M", "3M", "1Y"] if difficulty >= 2 else ["1M", "3M"]))
    tau = TENORS[tenor]
    shocks = ["vol_up", "vol_down", "spot_up", "spot_down", "time"]
    if g == "delta" and mon == "ATM":
        shocks = ["spot_up", "spot_down", "vol_up"]
    kind = str(rng.choice(shocks))
    md = MONEYNESS[mon]
    s = build("call" if cp == "C" else "put", mkt, tenor, 1e7, moneyness_delta=md)
    m1, shock_text = _shock(rng, mkt, kind, tau, difficulty)
    e0, e1 = s.exposure(mkt), s.exposure(m1)
    b, a = getattr(e0, g), getattr(e1, g)
    word = direction_word(b, a)
    opt = f"{mon} {'call' if cp == 'C' else 'put'}"
    gname = GREEK_LABEL[g]
    prompt = (f"You are long a {tenor_text(tenor)} {pair} {opt} (notional {pair[:3]} 10m, "
              f"strike {s.legs[0].K:.{mkt.pair.decimals}f}, spot {mkt.spot:.{mkt.pair.decimals}f}).\n\n"
              f"**Shock:** {shock_text}.\n\nWhat happens to the size of its **{gname.lower()}**?")
    mech_key = (g, "time" if kind == "time" else kind)
    mech = MECH.get(mech_key, "")
    chg = (a - b) / abs(b) * 100 if b else 0.0
    model = (f"**Answer: {DIR_OPTIONS[DIR_MAP[word]]}.**\n\n"
             f"1. Intuition: {mech}\n"
             f"2. This option: {gname.lower()} goes from {fmt_greek(mkt, g, b)} to {fmt_greek(mkt, g, a)} "
             f"({chg:+.1f}%), measured in {GREEK_UNITS[g]}.\n")
    if g == "delta":
        model += (f"3. As a fraction of notional: {b/1e7:+.3f} to {a/1e7:+.3f}.\n")
    facts = {"pair": pair, "option": opt, "tenor": tenor, "shock": shock_text, "greek": gname,
             "before": b, "after": a, "pct_change": chg, "direction_of_size": word,
             "delta_before_frac": e0.delta / 1e7, "delta_after_frac": e1.delta / 1e7}
    spots = spot_grid(mkt, tau)
    series = {"Before": profile(s, mkt, g, spots)}
    if kind not in ("spot_up", "spot_down"):
        series["After"] = profile(s, m1, g, spots)
    title = f"{gname} vs spot" + (" (spot move: same curve, new point)" if "spot" in kind else ", before and after")
    charts = [chart_line(title, spots, series, "Spot", f"{gname} ({GREEK_UNITS[g]})",
                         vline=m1.spot, vline_label="spot after")]
    return Question(
        section="options", subsection="1A", topic=f"greeks:{g.replace('_1pct','')}", difficulty=difficulty,
        template="direction", seed=seed, prompt=prompt,
        parts=[Part("mcq", f"Direction of {gname.lower()} (size)", DIR_OPTIONS, DIR_MAP[word])],
        free_text_prompt="Why? (one or two sentences)", facts=facts, model_answer=model,
        rubric=[f"Direction: {word}", f"Mechanism: {mech}"], charts=charts,
        tags=[g, kind, mon])


def q_compare(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    """Which of two options has more gamma / vega / theta?"""
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    g = str(rng.choice(["gamma_1pct", "vega", "theta"]))
    if difficulty == 1:
        t1, t2 = rng.choice([("1W", "3M"), ("1M", "1Y"), ("2W", "6M")])
        m1, m2 = "ATM", "ATM"
    else:
        if rng.random() < 0.5:
            t1, t2 = rng.choice([("1W", "3M"), ("1M", "1Y"), ("ON", "1M"), ("2W", "6M")])
            m1 = m2 = str(rng.choice(["ATM", "25-delta OTM"]))
        else:
            t1 = t2 = str(rng.choice(["1W", "1M", "3M"]))
            m1, m2 = "ATM", str(rng.choice(["25-delta OTM", "10-delta OTM"]))
    if rng.random() < 0.5:
        t1, t2, m1, m2 = t2, t1, m2, m1
    sA = build("call", mkt, t1, 1e7, moneyness_delta=MONEYNESS[m1])
    sB = build("call", mkt, t2, 1e7, moneyness_delta=MONEYNESS[m2])
    a, b = getattr(sA.exposure(mkt), g), getattr(sB.exposure(mkt), g)
    gname = GREEK_LABEL[g]
    A = f"A: {t1} {m1} call"
    B = f"B: {t2} {m2} call"
    ratio = abs(a) / abs(b)
    correct = 0 if abs(a) > abs(b) * 1.03 else 1 if abs(b) > abs(a) * 1.03 else 2
    opts = [A, B, "About the same"]
    why = {
        "gamma_1pct": "ATM gamma ~ e^(-rf T) n(d1) / (S vol sqrt(T)): the shorter the expiry the more concentrated (and larger) gamma is near the strike. For OTM strikes this reverses close to expiry, because the strike becomes many standard deviations away.",
        "vega": "Vega ~ S e^(-rf T) n(d1) sqrt(T): longer expiries carry more vega because there is more time for vol to matter. At a given expiry ATM has the most vega; OTM has less (n(d1) is smaller).",
        "theta": "ATM theta ~ -S n(d1) vol / (2 sqrt(T)): short-dated ATM options decay fastest per day. That is the flip side of their larger gamma (gamma/theta trade-off).",
    }[g]
    model = (f"**Answer: {opts[correct]}.**\n\n1. Intuition: {why}\n"
             f"2. Engine numbers (EUR/base 10m each): A = {fmt_greek(mkt, g, a)}, B = {fmt_greek(mkt, g, b)}; "
             f"|A|/|B| = {ratio:.2f}.\n")
    if g == "gamma_1pct" and m1 == m2 == "ATM":
        model += f"3. Rule of thumb: ATM gamma ratio ~ sqrt(T_B / T_A) = {np.sqrt(TENORS[t2]/TENORS[t1]):.2f}.\n"
    if g == "vega" and m1 == m2 == "ATM":
        model += f"3. Rule of thumb: ATM vega ratio ~ sqrt(T_A / T_B) = {np.sqrt(TENORS[t1]/TENORS[t2]):.2f}.\n"
    facts = {"pair": pair, "greek": gname, "A": A, "B": B, "A_value": a, "B_value": b, "ratio_abs_A_over_B": ratio}
    return Question(section="options", subsection="1A", topic=f"greeks:{g.replace('_1pct','')}",
                    difficulty=difficulty, template="compare", seed=seed,
                    prompt=f"{pair}, same notional. Which option has more **{gname.lower()}** (in size)?\n\n- {A}\n- {B}",
                    parts=[Part("mcq", "Which has more?", opts, correct)],
                    free_text_prompt="Why?", facts=facts, model_answer=model,
                    rubric=[f"Answer {opts[correct]}", why],
                    charts=[chart_bar(f"{gname}: A vs B", ["A", "B"], [a, b], f"{gname} ({GREEK_UNITS[g]})")])


def q_time_scaling(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    """Long 1Y ATM straddle, months pass: vega/gamma/theta as a multiple of the original."""
    pair = pick_pair(rng)
    base = fx_market(pair)
    v = base.vol(base.forward(1.0), 1.0)
    mkt = flat_market(base.pair, base.spot, base.rd, base.rf, v)
    months = int(rng.choice([3, 6, 9])) if difficulty >= 2 else 6
    g = "vega" if difficulty == 1 else str(rng.choice(["vega", "gamma_1pct", "theta"]))
    s = build("straddle", mkt, "1Y", 1e7)
    m1 = mkt.pass_time(months / 12 * 365)
    e0, e1 = s.exposure(mkt), s.exposure(m1)
    r = getattr(e1, g) / getattr(e0, g)
    rem = 1 - months / 12
    rule = {"vega": np.sqrt(rem), "gamma_1pct": 1 / np.sqrt(rem), "theta": 1 / np.sqrt(rem)}[g]
    gname = GREEK_LABEL[g]
    rule_txt = {"vega": "vega ~ sqrt(T)", "gamma_1pct": "gamma ~ 1/sqrt(T)", "theta": "theta ~ 1/sqrt(T)"}[g]
    model = (f"**Answer: about {r:.2f}x the original.**\n\n"
             f"1. Intuition: with spot and vol unchanged the straddle stays at the money, so only time matters. "
             f"For ATM options {rule_txt}.\n"
             f"2. Remaining time is {rem:.2f}y, so the rule of thumb gives {rule:.2f}x.\n"
             f"3. Engine: {gname.lower()} goes from {fmt_greek(mkt, g, getattr(e0, g))} to "
             f"{fmt_greek(mkt, g, getattr(e1, g))}, i.e. {r:.3f}x (the small gap to the rule comes from rates "
             f"and the strike drifting slightly off the new ATM).\n")
    return Question(section="options", subsection="1A", topic=f"greeks:{g.replace('_1pct','')}",
                    difficulty=difficulty, template="time_scaling", seed=seed,
                    prompt=(f"You are long a 1Y ATM {pair} straddle (vol {v*100:.1f}%). {months} months pass with "
                            f"spot and implied vol unchanged. Roughly what is your **{gname.lower()}** now, as a "
                            f"multiple of the original?"),
                    parts=[Part("numeric", "Multiple of original (e.g. 0.71)", correct=float(r), tol_abs=0.06, unit="x")],
                    free_text_prompt="Explain the scaling.",
                    facts={"pair": pair, "greek": gname, "months_passed": months, "ratio": r,
                           "rule_of_thumb": rule, "before": getattr(e0, g), "after": getattr(e1, g)},
                    model_answer=model, rubric=[f"Ratio about {r:.2f}", f"Uses {rule_txt}", "Explains that the straddle stays ATM"])


def q_vega_buckets(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    """Total vega +X but vols move by tenor: compute the actual P&L."""
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    target_total = float(rng.choice([100e3, 150e3, 200e3]))
    split = float(rng.choice([0.3, 0.4, 0.5, 0.6, 0.7]))
    short = build("straddle", mkt, "1M", 1.0)
    long_ = build("straddle", mkt, "1Y", 1.0)
    vs, vl = short.exposure(mkt).vega, long_.exposure(mkt).vega
    n_s = split * target_total / vs
    n_l = (1 - split) * target_total / vl
    if difficulty >= 3 and rng.random() < 0.5:
        n_l = -n_l * 0.6  # short the back end: total vega lower, opposite signs
    book_legs = short.scaled(n_s).legs + long_.scaled(n_l).legs
    from engine.structures import Structure
    book = Structure("book", book_legs)
    e = book.exposure(mkt)
    d1m = round(float(rng.uniform(1.0, 3.0)), 1)
    d1y = round(float(rng.uniform(0.2, 0.8)) * (1 if rng.random() < 0.8 else -1), 1)
    w = lambda tau: d1m if tau < 0.5 else d1y
    m1 = mkt.bump_vol(1.0, w)
    pnl = book.value(m1) - book.value(mkt)
    vb = e.vega_by_tenor
    naive = e.vega * d1m
    model = (f"**Answer: about {pnl/1e3:,.0f}k {mkt.pair.quote}, not {naive/1e3:,.0f}k.**\n\n"
             f"1. Intuition: 'vega per vol point' assumes every tenor moves by the same amount. Vol term "
             f"structures rarely move in parallel: front-end vols move several times more than back-end vols "
             f"(roughly in proportion to 1/sqrt(T)), so you must bucket vega by tenor.\n"
             f"2. Buckets: 1M vega = {vb.get('1M', 0)/1e3:,.0f}k, 1Y vega = {vb.get('1Y', 0)/1e3:,.0f}k per vol pt.\n"
             f"3. P&L ~ sum(vega_i x dvol_i) = {vb.get('1M', 0)/1e3:,.0f}k x {d1m} + "
             f"{vb.get('1Y', 0)/1e3:,.0f}k x {d1y} = {(vb.get('1M',0)*d1m + vb.get('1Y',0)*d1y)/1e3:,.0f}k "
             f"(full revaluation: {pnl/1e3:,.0f}k; the difference is volga).\n"
             f"4. Desks often also look at 'weighted vega' (vega scaled by sqrt(T_ref/T)) to compare tenors.\n")
    return Question(section="options", subsection="1A", topic="greeks:vega_buckets", difficulty=difficulty,
                    template="vega_buckets", seed=seed,
                    prompt=(f"Your {pair} book shows total vega of **{e.vega/1e3:+,.0f}k {mkt.pair.quote} per vol "
                            f"point** ({vb.get('1M',0)/1e3:+,.0f}k in 1M, {vb.get('1Y',0)/1e3:+,.0f}k in 1Y). "
                            f"1M vol rises {d1m} points and 1Y vol moves {d1y:+} points. What is your vega P&L, "
                            f"in thousands? Why can't you just multiply total vega by the 1M move?"),
                    parts=[Part("numeric", f"Vega P&L (k {mkt.pair.quote})", correct=pnl / 1e3,
                                tol_abs=max(2.0, 0.05 * abs(pnl / 1e3)), unit="k")],
                    free_text_prompt="Explain why the naive answer is wrong.",
                    facts={"pair": pair, "vega_total": e.vega, "vega_by_tenor": vb, "dvol_1M": d1m, "dvol_1Y": d1y,
                           "pnl_full_reval": pnl, "naive_total_vega_x_1M_move": naive},
                    model_answer=model,
                    rubric=["Vega must be bucketed by tenor", "Front-end vol moves more than back-end",
                            f"P&L about {pnl/1e3:,.0f}k"])


def q_sign(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    """Sign of vanna / volga / charm for a vanilla (hard level)."""
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    g = str(rng.choice(["vanna", "volga", "charm"]))
    mon = str(rng.choice(["ATM", "25-delta OTM", "10-delta OTM"]))
    cp = str(rng.choice(["C", "P"]))
    tenor = str(rng.choice(["1M", "3M"]))
    s = build("call" if cp == "C" else "put", mkt, tenor, 1e7, moneyness_delta=MONEYNESS[mon])
    v = getattr(s.exposure(mkt), g)
    ref_s = build("call", mkt, tenor, 1e7, moneyness_delta=0.25)
    ref = abs(getattr(ref_s.exposure(mkt), g))
    sgn = "0" if abs(v) < 0.15 * ref else ("+" if v > 0 else "-")
    opts = ["Positive", "Negative", "Roughly zero"]
    correct = {"+": 0, "-": 1, "0": 2}[sgn]
    opt = f"{mon} {'call' if cp == 'C' else 'put'}"
    why = {
        "vanna": ("Vanna = d(delta)/d(vol). Raising vol pulls deltas towards 50: an OTM call's delta rises "
                  "(positive vanna); an OTM put's delta goes from -0.25 towards -0.5, i.e. falls (negative vanna). "
                  "ATM delta barely moves, so ATM vanna is near zero."),
        "volga": ("Volga = d(vega)/d(vol). ATM vega is almost linear in vol (volga ~ 0). Wing options gain "
                  "vega as vol rises because the strike becomes 'closer' in standard deviations, so long OTM "
                  "options have positive volga, for calls and puts alike."),
        "charm": ("Charm = change in delta as time passes. With less time, an OTM option's delta decays "
                  "towards 0: an OTM call's delta falls (negative charm), an OTM put's delta rises towards 0 "
                  "(positive charm). ATM charm is small and driven by rates and the strike's offset from the forward."),
    }[g]
    model = (f"**Answer: {opts[correct]}.**\n\n1. Intuition: {why}\n2. Engine: {g} of this long {opt} = "
             f"{fmt_greek(mkt, g, v)} (reference 25d call: {fmt_greek(mkt, g, ref)}).\n")
    return Question(section="options", subsection="1A", topic=f"greeks:{g}", difficulty=difficulty,
                    template="sign", seed=seed,
                    prompt=f"You are long a {tenor} {pair} {opt}. What is the sign of its **{g}**?",
                    parts=[Part("mcq", f"Sign of {g}", opts, correct)], free_text_prompt="Why?",
                    facts={"pair": pair, "option": opt, "greek": g, "value": v, "reference_25d_call": ref},
                    model_answer=model, rubric=[f"Sign {opts[correct]}", why])


TEMPLATES = {1: [q_direction, q_compare, q_time_scaling],
             2: [q_direction, q_compare, q_time_scaling, q_vega_buckets],
             3: [q_direction, q_compare, q_time_scaling, q_vega_buckets, q_sign, q_sign]}


def generate(seed: int, difficulty: int) -> Question:
    rng = np.random.default_rng(seed)
    fn = TEMPLATES[difficulty][int(rng.integers(len(TEMPLATES[difficulty])))]
    return fn(rng, difficulty, seed)

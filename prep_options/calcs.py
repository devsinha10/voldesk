"""Calculation questions (Level 3) for Sections 1A and 1C.

Every numeric answer comes from ``solver(givens)``, which reads ONLY the
givens shown in the Givens box. The engine's exact number is shown in the
model answer next to the formula result, with the gap explained.
"""
from __future__ import annotations

import numpy as np

from engine.fx_conventions import TENORS
from engine.fx_pricer import price
from engine.structures import Structure, build, flat_market
from grading.question import Part, Question, attach_givens
from prep_options.common import fx_market, pick_pair, static_market

DIR3 = ["Increases", "Decreases", "Roughly unchanged"]


def q_time_scaling(rng, level, seed, subsection="1A"):
    pair = pick_pair(rng)
    base = fx_market(pair)
    v = base.vol(base.forward(1.0), 1.0)
    mkt = flat_market(base.pair, base.spot, base.rd, base.rf, v)
    months = int(rng.choice([3, 6, 9]))
    g = str(rng.choice(["vega", "gamma_1pct", "theta"]))
    s = build("straddle", mkt, "1Y", 1e7)
    e0, e1 = s.exposure(mkt), s.exposure(mkt.pass_time(months / 12 * 365))
    name = {"vega": "vega", "gamma_1pct": "gamma", "theta": "theta"}[g]
    unit = {"vega": f"{mkt.pair.quote} per vol pt", "gamma_1pct": f"{mkt.pair.base} delta per 1% spot",
            "theta": f"{mkt.pair.quote} per day"}[g]
    givens = {"greek": name, "T0": 1.0, "T1": round(1 - months / 12, 4), "before": round(getattr(e0, g), 0)}
    labels = {"greek": "Greek", "T0": "Time to expiry now (years)", "T1": "Time to expiry later (years)",
              "before": f"Your {name} now ({unit})"}

    def solver(gv):
        r = np.sqrt(gv["T1"] / gv["T0"])
        return [gv["before"] * (r if gv["greek"] == "vega" else 1 / r)]

    exact = getattr(e1, g)
    up = g != "vega"
    q = Question("options", subsection, f"greeks:{name}", level, "time_scaling", seed,
                 prompt=(f"You are long a 1Y ATM {pair} straddle (vol {v*100:.1f}%, {pair[:3]} 10m per leg). "
                         f"{months} months pass with spot and implied vol unchanged. Which way does your {name} move, "
                         f"and roughly what is it now?"),
                 parts=[Part("mcq", f"Direction of {name} (size)", DIR3, 0 if up else 1),
                        Part("numeric", f"New {name} ({unit})", tol_rel=0.06)],
                 free_text_prompt="Explain the scaling.",
                 rubric=[f"ATM {name} scales with {'sqrt(T)' if g == 'vega' else '1/sqrt(T)'}",
                         f"{name} {'rises' if up else 'falls'}"])
    attach_givens(q, givens, labels, solver)
    est = q.parts[1].correct
    q.model_answer = (f"**{name.capitalize()} {'rises' if up else 'falls'} to about {est:,.0f} {unit}.**\n\n"
                      f"1. Intuition: spot and vol are unchanged, so the straddle stays at the money and only time "
                      f"matters. ATM vega ~ S n(d1) sqrt(T); ATM gamma ~ n(d1) / (S vol sqrt(T)); ATM theta ~ "
                      f"-S n(d1) vol / (2 sqrt(T)).\n"
                      f"2. Formula: {name}_later = {name}_now x {'sqrt(T1/T0)' if g == 'vega' else 'sqrt(T0/T1)'} = "
                      f"{givens['before']:,.0f} x {(np.sqrt(givens['T1']) if g == 'vega' else 1/np.sqrt(givens['T1'])):.3f} "
                      f"= {est:,.0f}.\n"
                      f"3. Engine (full revaluation): {exact:,.0f}. The gap ({(exact/est - 1)*100:+.1f}%) comes from "
                      f"rates and the strike drifting slightly off the new ATM (d1 is not exactly 0).")
    q.facts = {**givens, "engine_exact": exact}
    return q


def q_rv_iv(rng, level, seed, subsection="1A"):
    pair = pick_pair(rng)
    base = fx_market(pair)
    tau = TENORS["1M"]
    vi = round(base.vol(base.forward(tau), tau) * 100, 1)
    vr = round(vi + float(rng.choice([-3, -2, 2, 3, 4])), 1)
    days = int(rng.choice([5, 10]))
    mkt = flat_market(base.pair, base.spot, base.rd, base.rf, vi / 100)
    e = build("straddle", mkt, "1M", 1e7).exposure(mkt)
    givens = {"S": round(mkt.spot, 5), "gamma_1pct": round(e.gamma_1pct, 0), "vol_implied": vi,
              "vol_realised": vr, "days": days}
    labels = {"S": "Spot", "gamma_1pct": f"Gamma ({mkt.pair.base} delta change per 1% spot move)",
              "vol_implied": "Implied vol paid (%)", "vol_realised": "Realised vol (%)", "days": "Days held (calendar)"}

    def solver(gv):
        gamma_unit = gv["gamma_1pct"] / (0.01 * gv["S"])        # d2V/dS2 of the position
        var_gap = (gv["vol_realised"] / 100) ** 2 - (gv["vol_implied"] / 100) ** 2
        return [0.5 * gamma_unit * gv["S"] ** 2 * var_gap * gv["days"] / 365]

    q = Question("options", subsection, "concepts:implied_vs_realised", level, "rv_iv", seed,
                 prompt=(f"You are long a delta-hedged 1M ATM {pair} straddle. Over the next {days} days spot realises "
                         f"{vr:.1f}% vol while implied stays at {vi:.1f}%. Do you make or lose money, and roughly how "
                         f"much (in {mkt.pair.quote}, holding gamma constant)?"),
                 parts=[Part("mcq", "Sign of P&L", ["Profit", "Loss"], 0 if vr > vi else 1),
                        Part("numeric", f"P&L ({mkt.pair.quote})", tol_rel=0.08)],
                 free_text_prompt="Explain where the P&L comes from and why the estimate is approximate.",
                 rubric=["P&L ~ 0.5 Gamma S^2 (realised^2 - implied^2) dt", "Sign from realised vs implied",
                         "Gamma changes / path dependence"])
    attach_givens(q, givens, labels, solver)
    p = q.parts[1].correct
    q.model_answer = (f"**{'Profit' if p > 0 else 'Loss'} of about {p:,.0f} {mkt.pair.quote}.**\n\n"
                      f"1. Intuition: a delta-hedged option earns 0.5 Gamma dS^2 on each move and pays theta, which is "
                      f"priced at the implied vol. Net, you earn the gap between realised and implied variance.\n"
                      f"2. Gamma in d2V/dS2 terms = gamma_1pct / (1% x S) = {givens['gamma_1pct']:,.0f} / "
                      f"{0.01 * givens['S']:.5g} = {givens['gamma_1pct'] / (0.01 * givens['S']):,.0f}.\n"
                      f"3. P&L ~ 0.5 x Gamma x S^2 x (realised^2 - implied^2) x days/365 = {p:,.0f}.\n"
                      f"4. Approximate because gamma changes as spot moves and time passes, and the P&L depends on when "
                      f"the moves happen (path dependence).")
    q.facts = dict(givens)
    return q


def q_breakeven(rng, level, seed, subsection="1A"):
    pair = pick_pair(rng)
    base = fx_market(pair)
    tenor = str(rng.choice(["1W", "1M", "3M"]))
    tau = TENORS[tenor]
    v = base.vol(base.forward(tau), tau)
    mkt = flat_market(base.pair, base.spot, base.rd, base.rf, v)
    e = build("straddle", mkt, tenor, 1e7).exposure(mkt)
    givens = {"S": round(mkt.spot, 5), "theta": round(e.theta, 0), "gamma_1pct": round(e.gamma_1pct, 0)}
    labels = {"S": "Spot", "theta": f"Theta ({mkt.pair.quote} per day)",
              "gamma_1pct": f"Gamma ({mkt.pair.base} delta change per 1% spot move)"}

    def solver(gv):
        gamma_unit = gv["gamma_1pct"] / (0.01 * gv["S"])
        dS = np.sqrt(2 * abs(gv["theta"]) / gamma_unit)
        return [dS / gv["S"] * 100]

    rv_daily = round(float(rng.choice([0.6, 0.8, 1.2, 1.5])) * v * 100 / np.sqrt(365), 2)
    q = Question("options", subsection, "concepts:gamma_theta", level, "breakeven", seed,
                 prompt=(f"You buy a {tenor} ATM {pair} straddle ({pair[:3]} 10m per leg) at {v*100:.2f}% vol and "
                         f"delta-hedge it. How big a daily move (in %) do you need to break even on theta? If spot "
                         f"then moves {rv_daily:.2f}% a day on average, do you make or lose money?"),
                 parts=[Part("numeric", "Breakeven daily move (%)", tol_rel=0.05, unit="%"),
                        Part("mcq", f"With {rv_daily:.2f}% daily moves", ["Make money", "Lose money"], 0)],
                 free_text_prompt="Explain the gamma/theta trade-off.",
                 rubric=["0.5 Gamma dS^2 = |theta|", "Breakeven ~ vol / sqrt(365)", "Compare realised to breakeven"])
    attach_givens(q, givens, labels, solver)
    be = q.parts[0].correct
    q.parts[1].correct = 0 if rv_daily > be else 1
    q.model_answer = (f"**About {be:.2f}% a day; with {rv_daily:.2f}% moves you {'make' if rv_daily > be else 'lose'} money.**\n\n"
                      f"1. Each day you earn 0.5 x Gamma x dS^2 and pay |theta|. Break even when they are equal: "
                      f"dS = sqrt(2|theta| / Gamma).\n"
                      f"2. Gamma = {givens['gamma_1pct']:,.0f} / (1% x {givens['S']}) = "
                      f"{givens['gamma_1pct'] / (0.01 * givens['S']):,.0f}; dS = {be/100*givens['S']:.5g}, i.e. {be:.2f}%.\n"
                      f"3. Check: theta ~ -0.5 Gamma S^2 vol^2 / 365, so the breakeven is about vol / sqrt(365) = "
                      f"{v*100:.2f}% / 19.1 = {v*100/np.sqrt(365):.2f}%. Realised above implied wins.")
    q.facts = {**givens, "vol": v, "daily_move_tested": rv_daily}
    return q


def q_vega_buckets(rng, level, seed, subsection="1A"):
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    tot = float(rng.choice([100e3, 150e3, 200e3]))
    split = float(rng.choice([0.3, 0.5, 0.7]))
    sh, lo = build("straddle", mkt, "1M", 1.0), build("straddle", mkt, "1Y", 1.0)
    n_s, n_l = split * tot / sh.exposure(mkt).vega, (1 - split) * tot / lo.exposure(mkt).vega
    if rng.random() < 0.4:
        n_l = -0.6 * n_l
    book = Structure("book", sh.scaled(n_s).legs + lo.scaled(n_l).legs)
    vb = book.exposure(mkt).vega_by_tenor
    d1 = round(float(rng.uniform(1.0, 3.0)), 1)
    d2 = round(float(rng.uniform(0.2, 0.8)) * (1 if rng.random() < 0.8 else -1), 1)
    exact = book.value(mkt.bump_vol(1.0, lambda t: d1 if t < 0.5 else d2)) - book.value(mkt)
    givens = {"vega_1M": round(vb.get("1M", 0), 0), "vega_1Y": round(vb.get("1Y", 0), 0), "dvol_1M": d1, "dvol_1Y": d2}
    labels = {"vega_1M": f"1M vega ({mkt.pair.quote} per vol pt)", "vega_1Y": f"1Y vega ({mkt.pair.quote} per vol pt)",
              "dvol_1M": "1M vol move (pts)", "dvol_1Y": "1Y vol move (pts)"}

    def solver(gv):
        return [(gv["vega_1M"] * gv["dvol_1M"] + gv["vega_1Y"] * gv["dvol_1Y"]) / 1e3]

    naive = (givens["vega_1M"] + givens["vega_1Y"]) * d1 / 1e3
    q = Question("options", subsection, "greeks:vega_buckets", level, "vega_buckets", seed,
                 prompt=(f"Your {pair} book's vega is in two buckets (see Givens). 1M vol moves {d1:+} and 1Y moves "
                         f"{d2:+}. What is your vega P&L in thousands? Is it bigger or smaller than total vega x the 1M "
                         f"move ({naive:,.0f}k)?"),
                 parts=[Part("numeric", f"Vega P&L (k {mkt.pair.quote})", tol_abs=1.0, tol_rel=0.03),
                        Part("mcq", "Compared with the naive number", ["Bigger", "Smaller"], 0)],
                 free_text_prompt="Why must vega be bucketed by tenor?",
                 rubric=["Vega P&L = sum of bucket vega x bucket vol move", "Front vols move more than back vols"])
    attach_givens(q, givens, labels, solver)
    est = q.parts[0].correct
    q.parts[1].correct = 0 if est > naive else 1
    q.model_answer = (f"**About {est:,.0f}k, vs {naive:,.0f}k naive.**\n\n1. Vol term structures rarely move in "
                      f"parallel: front vols move several times more than back vols, so vega is bucketed by tenor.\n"
                      f"2. P&L ~ {givens['vega_1M']:,.0f} x {d1} + {givens['vega_1Y']:,.0f} x {d2} = {est*1e3:,.0f}.\n"
                      f"3. Engine full revaluation: {exact:,.0f} (gap from volga, the change in vega as vol moves).")
    q.facts = {**givens, "engine_exact": exact}
    return q


# ---------------------------------------------------------------------------
# 1C Level 3: sticky strike with numbers, arbitrage with numbers
# ---------------------------------------------------------------------------
def q_sticky_calc(rng, level, seed, subsection="1C"):
    pair = str(rng.choice(["USDJPY", "AUDUSD", "USDCAD", "EURUSD", "USDCHF"]))
    mkt = fx_market(pair)
    sm = static_market().surface(pair).smiles["1M"]
    pct = round(float(rng.uniform(1.0, 2.5)) * (1 if rng.random() < 0.5 else -1), 1)
    tau = TENORS["1M"]
    k0 = mkt.atm_strike(tau)
    v0 = mkt.vol(k0, tau)
    ms = mkt.bump_spot(pct)
    exact = (ms.vol(ms.atm_strike(tau), tau) - v0) * 100
    dec = mkt.pair.decimals
    givens = {"K_ATM": round(k0, dec), "vol_ATM": round(v0 * 100, 3),
              "K_25C": round(sm.pillar_strikes["25C"], dec), "vol_25C": round(sm.pillar_vols["25C"] * 100, 3),
              "K_25P": round(sm.pillar_strikes["25P"], dec), "vol_25P": round(sm.pillar_vols["25P"] * 100, 3),
              "spot_move_pct": pct}
    labels = {"K_ATM": "ATM strike now", "vol_ATM": "ATM vol (%)", "K_25C": "25d call strike", "vol_25C": "25d call vol (%)",
              "K_25P": "25d put strike", "vol_25P": "25d put vol (%)", "spot_move_pct": "Spot move (%)"}

    def solver(gv):
        k_new = gv["K_ATM"] * (1 + gv["spot_move_pct"] / 100)
        if k_new >= gv["K_ATM"]:
            slope = (gv["vol_25C"] - gv["vol_ATM"]) / (gv["K_25C"] - gv["K_ATM"])
        else:
            slope = (gv["vol_ATM"] - gv["vol_25P"]) / (gv["K_ATM"] - gv["K_25P"])
        return [slope * (k_new - gv["K_ATM"])]

    opts = ["Rises", "Falls", "Unchanged"]
    q = Question("options", subsection, "concepts:sticky", level, "sticky_calc", seed,
                 prompt=(f"{pair} 1M smile in the Givens. Spot moves {pct:+.1f}% and the ATM strike moves with it. "
                         f"Under **sticky strike**, estimate the change in 1M ATM vol (vol pts) by linear interpolation "
                         f"between the pillars. What happens under **sticky delta**?"),
                 parts=[Part("numeric", "Change in ATM vol, sticky strike (vol pts)", tol_abs=0.03, tol_rel=0.15),
                        Part("mcq", "ATM vol under sticky delta", opts, 2)],
                 free_text_prompt="Explain the difference and when traders assume each.",
                 rubric=["Sticky strike: read the old smile at the new ATM strike", "Sticky delta: ATM vol unchanged",
                         "Sign follows the skew on that side"])
    attach_givens(q, givens, labels, solver)
    est = q.parts[0].correct
    q.model_answer = (f"**Sticky strike: about {est:+.2f} vol pts. Sticky delta: unchanged.**\n\n"
                      f"1. Sticky strike: each strike keeps its vol, so the new ATM strike "
                      f"({givens['K_ATM'] * (1 + pct/100):.{dec}f}) reads the old smile on the "
                      f"{'call' if pct > 0 else 'put'} side.\n"
                      f"2. Linear interpolation between ATM and the 25d {'call' if pct > 0 else 'put'} pillar gives {est:+.3f}.\n"
                      f"3. Engine (SABR smile, exact ATM strike): {exact:+.3f}; the gap is the smile's curvature.\n"
                      f"4. Sticky delta: the smile moves with spot, so ATM vol is unchanged. Traders lean sticky strike "
                      f"in calm, range-bound markets and sticky delta (or worse, 'sticky moneyness with skew') in trending "
                      f"or stressed markets; the choice changes your smile-adjusted delta.")
    q.facts = {**givens, "engine_exact": exact}
    return q


def q_arb_calc(rng, level, seed, subsection="1C"):
    v = str(rng.choice(["call_spread", "butterfly", "calendar", "parity"]))
    if v == "call_spread":
        K1 = float(rng.choice([95, 100, 105])); w = float(rng.choice([5, 10]))
        r, T = float(rng.choice([0.03, 0.04, 0.05])), float(rng.choice([0.5, 1.0]))
        p = round(w * np.exp(-r * T) + float(rng.uniform(0.2, 1.0)), 2)
        givens = {"K1": K1, "K2": K1 + w, "price": p, "r": r, "T": T}
        labels = {"K1": "Lower strike", "K2": "Upper strike", "price": "Call spread price", "r": "Rate (cont. comp.)",
                  "T": "Expiry (years)"}
        solver = lambda g: [g["price"] - (g["K2"] - g["K1"]) * np.exp(-g["r"] * g["T"])]
        prompt = f"A {T:g}y {K1:.0f}/{K1+w:.0f} call spread trades at {p:.2f} (rates in Givens). What is the arbitrage, and the PV profit locked in per unit?"
        opts = ["Sell the spread and invest the proceeds", "Buy the spread", "No arbitrage"]
        why = "A call spread pays at most K2 - K1 at expiry, so it can never be worth more than (K2 - K1) e^(-rT) today."
    elif v == "butterfly":
        S, sig, T = 100.0, float(rng.choice([0.15, 0.2, 0.25])), 0.5
        C = [float(price(S, K, T, 0, 0, sig, "C")) for K in (90, 100, 110)]
        C[1] += (C[0] - 2 * C[1] + C[2]) / 2 + float(rng.uniform(0.2, 0.6))
        givens = {"C90": round(C[0], 2), "C100": round(C[1], 2), "C110": round(C[2], 2)}
        labels = {"C90": "90 call", "C100": "100 call", "C110": "110 call"}
        solver = lambda g: [-(g["C90"] - 2 * g["C100"] + g["C110"])]
        prompt = "Three calls on the same expiry (zero rates) are priced in the Givens. Is there an arbitrage? What credit do you lock in per unit?"
        opts = ["Buy the 90/100/110 butterfly for a credit", "Sell the butterfly", "No arbitrage"]
        why = "A 1x2x1 call fly pays >= 0 everywhere, so it must cost >= 0: call prices must be convex in strike."
    elif v == "calendar":
        c_far = round(float(price(100, 100, 0.5, 0, 0, 0.2, "C")), 2)
        c_near = round(c_far + float(rng.uniform(0.2, 0.8)), 2)
        givens = {"C_3M": c_near, "C_6M": c_far}
        labels = {"C_3M": "3M 100-strike call (spot 100)", "C_6M": "6M 100-strike call"}
        solver = lambda g: [g["C_3M"] - g["C_6M"]]
        prompt = "Zero rates, no dividends. Prices in the Givens. Is there an arbitrage? What credit do you lock in?"
        opts = ["Sell the 3M, buy the 6M (calendar for a credit)", "Buy the 3M, sell the 6M", "No arbitrage"]
        why = "With zero rates and no dividends a longer-dated call is worth at least the shorter one at the same strike."
    else:
        mkt = fx_market("EURUSD"); T = 0.25
        K = round(mkt.forward(T), 4)
        vv = mkt.vol(K, T)
        c = float(price(mkt.spot, K, T, mkt.rd, mkt.rf, vv, "C")); pp = float(price(mkt.spot, K, T, mkt.rd, mkt.rf, vv, "P"))
        mis = float(rng.choice([-1, 1])) * round(float(rng.uniform(8, 25))) * 1e-4
        givens = {"S": round(mkt.spot, 4), "K": K, "rd": round(mkt.rd, 4), "rf": round(mkt.rf, 4), "T": T,
                  "C_pips": round((c + mis) / 1e-4, 1), "P_pips": round(pp / 1e-4, 1)}
        labels = {"S": "EURUSD spot", "K": "Strike", "rd": "USD rate (cont.)", "rf": "EUR rate (cont.)", "T": "Expiry (years)",
                  "C_pips": "Call price (USD pips)", "P_pips": "Put price (USD pips)"}
        solver = lambda g: [abs((g["C_pips"] - g["P_pips"]) * 1e-4 -
                                (g["S"] * np.exp(-g["rf"] * g["T"]) - g["K"] * np.exp(-g["rd"] * g["T"]))) / 1e-4]
        rich = (givens["C_pips"] - givens["P_pips"]) * 1e-4 > givens["S"] * np.exp(-givens["rf"] * T) - K * np.exp(-givens["rd"] * T)
        prompt = "EURUSD 3M options in the Givens. Does put-call parity hold? What is the trade, and the mispricing in pips?"
        opts = ["Sell the call, buy the put, buy EUR forward", "Buy the call, sell the put, sell EUR forward", "No arbitrage"]
        why = "FX parity: C - P = S e^(-rf T) - K e^(-rd T)."
    correct = 0 if v != "parity" else (0 if rich else 1)
    q = Question("options", subsection, "concepts:arbitrage", level, f"arb_calc_{v}", seed, prompt=prompt,
                 parts=[Part("mcq", "Trade", opts, correct), Part("numeric", "Locked-in profit (per unit / pips)", tol_abs=0.02, tol_rel=0.02)],
                 free_text_prompt="Explain the bound being violated.", rubric=[why, opts[correct]])
    attach_givens(q, givens, labels, solver)
    q.model_answer = f"**{opts[correct]}; profit {q.parts[1].correct:.3f}.**\n\n1. {why}\n2. Plugging in the Givens gives {q.parts[1].correct:.4f}."
    q.facts = dict(givens)
    return q

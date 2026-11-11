"""Section 2A: who is long duration or convexity? Five unlockable stages, each
spread across three levels:

L1  intuition only: long/short duration and convexity, gain or lose, which is bigger and why
L2  combinations and light calculations with every input in the Givens box
L3  multi-step calculations (including computing D_mod / DV01 yourself) and subtler effects
"""
from __future__ import annotations

import math

import numpy as np

from engine.config import load_config
from engine.rates import bond_risk, par_swap_rate
from grading.question import attach_givens, chart_bar, chart_line
from prep_rates.instruments import (FRN, Bond, Composite, Swap, Swaption, base_curve, callable_bond, fmt_ccy,
                                    pnl, risk, sign_word)
from prep_rates.qkit import (GAIN_LOSE, LONG_SHORT, Q, approx_pnl, approx_vs_exact_text, bond_exact_pnl, bond_info,
                             dv01_gamma, mcq, num)

NVOL = load_config()["rates_engine"]["swaption_normal_vol_bp"] / 1e4
SIGN3 = ["+", "-", "0"]


def _pnl_chart(inst, c, title):
    moves = np.arange(-150, 151, 25)
    return chart_line(title, moves, {"P&L": [pnl(inst, c, c.shifted(m)) for m in moves]}, "Parallel move (bp)",
                      "P&L (GBP)", vline=0, vline_label="today")


def _bond_name(cpn: float, m: int) -> str:
    return f"{'zero-coupon' if cpn == 0 else f'{cpn*100:.2f}%'} {m}Y gilt"


# =============================================================================
# Stage 1: government bonds
# =============================================================================
def s1_l1_position(rng, lvl, seed):
    m = int(rng.choice([2, 5, 10, 30]))
    cpn = float(rng.choice([0.0, 0.0, 0.01, 0.04]))
    side = int(rng.choice([1, -1, -1]))  # more short positions
    bp = float(rng.choice([25, 50, 100]) * rng.choice([1, -1]))
    y = 0.04
    exact = side * bond_exact_pnl(100e6, cpn, m, y, bp)
    gains = exact > 0
    s = "long" if side > 0 else "short"
    model = (f"**{'Long' if side > 0 else 'Short'} duration, {'long' if side > 0 else 'short'} convexity; you "
             f"{'gain' if gains else 'lose'} if yields {'fall' if bp < 0 else 'rise'} {abs(bp):.0f}bp.**\n\n"
             f"1. A bond pays fixed cash flows; higher yields discount them more, so its price falls. Owning it = long "
             f"duration (you gain when yields fall). Being short flips it.\n"
             f"2. A vanilla bond's price/yield curve bends upward (positive convexity): long the bond = long convexity, "
             f"short the bond = SHORT convexity, so big moves either way hurt a short more than the duration term says.\n"
             f"3. Illustration (engine, full repricing): {fmt_ccy(exact)} for GBP 100m face.")
    return Q("2A-1", "duration:bond_basics", lvl, "s1_l1_position", seed,
             f"You are **{s} GBP 100m face of a {_bond_name(cpn, m)}**. Are you long or short duration? Long or short "
             f"convexity? Do you gain or lose if yields {'fall' if bp < 0 else 'rise'} {abs(bp):.0f}bp?",
             [mcq("Duration", LONG_SHORT, 0 if side > 0 else 1), mcq("Convexity", LONG_SHORT, 0 if side > 0 else 1),
              mcq(f"Yields {'fall' if bp < 0 else 'rise'} {abs(bp):.0f}bp", GAIN_LOSE, 0 if gains else 1)],
             "Explain each answer.", model,
             ["Long bond = long duration and long convexity; short flips both", "Gain/loss direction"],
             {"side": s, "bond": _bond_name(cpn, m), "move_bp": bp, "pnl_engine": exact})


def s1_l1_compare(rng, lvl, seed):
    y = 0.04
    kind = str(rng.choice(["zero_vs_coupon", "maturity", "coupon", "convexity_maturity"]))
    metric = "duration"
    if kind == "zero_vs_coupon":
        m = int(rng.choice([5, 10, 30])); A, B = (0.0, m), (0.05, m)
        why = "A zero pays everything at maturity; a coupon bond returns cash earlier, so its weighted-average time is shorter."
    elif kind == "maturity":
        A, B = (0.04, int(rng.choice([2, 5]))), (0.04, int(rng.choice([10, 30])))
        why = "Cash flows further away are discounted over more years, so their PV reacts more to yield."
    elif kind == "coupon":
        m = int(rng.choice([10, 30])); A, B = (0.01, m), (0.06, m)
        why = "A lower coupon leaves relatively more value in the final principal payment, pushing the weighted-average time out."
    else:
        metric = "convexity"
        A, B = (0.04, int(rng.choice([2, 5]))), (0.04, int(rng.choice([20, 30])))
        why = "Convexity grows roughly with maturity squared: the long bond's duration changes much more as yields move."
    if rng.random() < 0.5:
        A, B = B, A
    rA, rB = bond_risk(y, *A), bond_risk(y, *B)
    va, vb = (rA.modified, rB.modified) if metric == "duration" else (rA.convexity, rB.convexity)
    nm = lambda x: f"{'zero-coupon' if x[0] == 0 else f'{x[0]*100:.0f}%'} {x[1]}Y"
    corr = 0 if va > vb else 1
    return Q("2A-1", f"{metric}:drivers", lvl, "s1_l1_compare", seed,
             f"Which has more **{metric}**? A: a **{nm(A)}** bond. B: a **{nm(B)}** bond (same {y*100:.0f}% yield).",
             [mcq(f"More {metric}", ["A", "B"], corr)], "Why?",
             f"**{['A', 'B'][corr]}.**\n\n1. {why}\n2. Illustration (engine): A {metric} {va:.2f}, B {vb:.2f}.\n"
             f"3. Rules: duration rises with maturity, falls with coupon and yield; a zero's Macaulay duration equals its "
             f"maturity; convexity ~ maturity squared.",
             [why], {"A": nm(A), "B": nm(B), metric + "_A": va, metric + "_B": vb},
             charts=[chart_bar(metric.capitalize(), ["A", "B"], [va, vb], "")])


def s1_l1_asymmetry(rng, lvl, seed):
    m = int(rng.choice([10, 30]))
    side = int(rng.choice([1, -1]))
    bp = int(rng.choice([75, 100, 150]))
    up = side * bond_exact_pnl(100e6, 0.04, m, 0.04, bp)
    dn = side * bond_exact_pnl(100e6, 0.04, m, 0.04, -bp)
    bigger = 0 if abs(dn) > abs(up) else 1
    s = "own" if side > 0 else "are short"
    return Q("2A-1", "convexity:bond_basics", lvl, "s1_l1_asymmetry", seed,
             f"You {s} GBP 100m of a 4% {m}Y gilt. Compare your P&L if yields fall {bp}bp vs rise {bp}bp. "
             f"Which is larger in size, and why?",
             [mcq("Larger in size", ["The P&L from yields falling", "The P&L from yields rising", "They are equal"], bigger)],
             "Explain why.",
             f"**The {'rally' if bigger == 0 else 'selloff'} P&L is larger in size.**\n\n1. Positive convexity: as yields "
             f"fall duration lengthens, so price gains accelerate; as yields rise duration shortens, so losses slow down.\n"
             f"2. {'Long the bond: you gain more in the rally than you lose in the selloff.' if side > 0 else 'Short the bond (short convexity): you lose more in the rally than you gain in the selloff.'}\n"
             f"3. Illustration (engine): yields -{bp}bp {fmt_ccy(dn)}, +{bp}bp {fmt_ccy(up)}.",
             ["Convexity: duration lengthens as yields fall", "Sign of the asymmetry for long vs short"],
             {"pnl_down": dn, "pnl_up": up})


def s1_l2_sized(rng, lvl, seed):
    m = int(rng.choice([5, 10, 30])); cpn = float(rng.choice([0.0, 0.0425, 0.045]))
    y = float(rng.choice([0.035, 0.04, 0.045])); bp = float(rng.choice([25, 50, 100]) * rng.choice([1, -1]))
    side = int(rng.choice([1, -1])); face = 100e6
    info = bond_info(cpn, m, y)
    g = {"face": face * side, "price": round(info["price"], 4), "dmod": round(info["dmod"], 4),
         "convexity": round(info["convexity"], 3), "dy_bp": bp}
    labels = {"face": "Face (GBP, + long / - short)", "price": "Price (per 100)", "dmod": "Modified duration (years)",
              "convexity": "Convexity (years^2)", "dy_bp": "Yield move (bp, parallel)"}

    def solver(gv):
        d, c = approx_pnl(gv["face"], gv["price"], gv["dmod"], gv["convexity"], gv["dy_bp"])
        return [(d + c) / 1e3]
    q = Q("2A-1", "duration:sized_pnl", lvl, "s1_l2_sized", seed,
          f"You are {'long' if side > 0 else 'short'} GBP 100m face of a {_bond_name(cpn, m)}. Using the Givens, "
          f"estimate your P&L if yields move {bp:+.0f}bp. Are you long or short duration?",
          [num("P&L (GBP thousands)", "k", tol_rel=0.02, tol_abs=2), mcq("Duration", LONG_SHORT, 0 if side > 0 else 1)],
          "Show the duration and convexity terms.", "", ["dP ~ -D P dy + 0.5 C P dy^2", "Sign from long/short"])
    attach_givens(q, g, labels, solver)
    d, c = approx_pnl(g["face"], g["price"], g["dmod"], g["convexity"], bp)
    exact = side * bond_exact_pnl(face, cpn, m, y, bp)
    q.model_answer = f"**About {fmt_ccy(d + c)}.**\n\n" + approx_vs_exact_text(d, c, exact)
    q.facts = {**g, "exact": exact}
    q.charts = [_pnl_chart(Bond(cpn, m, face * side), base_curve(), "P&L vs parallel move (curve-based)")]
    return q


def s1_l2_asymmetry_sized(rng, lvl, seed):
    m = int(rng.choice([10, 30])); y = 0.04; bp = int(rng.choice([75, 100, 150])); face = 100e6
    info = bond_info(0.04, m, y)
    g = {"face": face, "price": round(info["price"], 4), "convexity": round(info["convexity"], 3), "dy_bp": bp}
    labels = {"face": "Face (GBP)", "price": "Price (per 100)", "convexity": "Convexity (years^2)",
              "dy_bp": "Size of the move (bp)"}
    solver = lambda gv: [gv["face"] / 100 * gv["convexity"] * gv["price"] * (gv["dy_bp"] * 1e-4) ** 2 / 1e3]
    q = Q("2A-1", "convexity:sized", lvl, "s1_l2_asym_sized", seed,
          f"You own GBP 100m of a 4% {m}Y gilt. By how much does your gain if yields fall {bp}bp exceed your loss "
          f"if they rise {bp}bp? Use the Givens.",
          [num("Gain minus |loss| (GBP thousands)", "k", tol_rel=0.08, tol_abs=2)], "Explain where the difference comes from.",
          "", ["Difference ~ C P dy^2 (twice the convexity term)", "Duration terms cancel"])
    attach_givens(q, g, labels, solver)
    exact = bond_exact_pnl(face, 0.04, m, y, -bp) + bond_exact_pnl(face, 0.04, m, y, bp)
    est = q.parts[0].correct * 1e3
    q.model_answer = (f"**About {fmt_ccy(est)}.**\n\n1. The duration terms are equal and opposite, so they cancel; the "
                      f"two convexity terms add: 2 x 0.5 C P dy^2 = C P dy^2 = {fmt_ccy(est)}.\n2. Exact (engine): "
                      f"{fmt_ccy(exact)}; gap {fmt_ccy(exact - est)} from higher-order terms.")
    q.facts = {**g, "exact": exact}
    return q


def s1_l3_compute(rng, lvl, seed):
    m = int(rng.choice([3, 5, 7])); cpn = float(rng.choice([0.03, 0.04, 0.05])); freq = int(rng.choice([1, 2]))
    y = float(rng.choice([0.035, 0.04, 0.045])); face = 100e6
    g = {"coupon_pct": cpn * 100, "maturity": m, "freq": freq, "yield_pct": y * 100, "face": face}
    labels = {"coupon_pct": "Coupon (% a year)", "maturity": "Maturity (years)", "freq": "Coupons per year",
              "yield_pct": "Yield (%, compounded at the coupon frequency)", "face": "Face (GBP)"}

    def solver(gv):
        r = bond_risk(gv["yield_pct"] / 100, gv["coupon_pct"] / 100, gv["maturity"], int(gv["freq"]))
        return [r.modified, gv["face"] / 100 * r.dv01]
    q = Q("2A-1", "duration:compute", lvl, "s1_l3_compute", seed,
          "Compute the bond's **modified duration** and the position's **DV01** from the bond details in the Givens.",
          [num("Modified duration (years)", "y", tol_rel=0.01), num("DV01 (GBP per bp)", tol_rel=0.01)],
          "Show the steps.", "", ["Macaulay = PV-weighted average time", "D_mod = D_mac / (1 + y/f)",
                                  "DV01 = D_mod x P x 1bp x face/100"])
    attach_givens(q, g, labels, solver)
    r = bond_risk(y, cpn, m, freq)
    q.model_answer = (f"**D_mod {r.modified:.3f}, DV01 {fmt_ccy(face / 100 * r.dv01)} per bp.**\n\n"
                      f"1. Price = sum of CF_k / (1 + y/f)^k = {r.price:.4f}.\n2. Macaulay = sum of t_k x PV_k / P = "
                      f"{r.macaulay:.4f} years.\n3. D_mod = D_mac / (1 + y/f) = {r.macaulay:.4f} / {1 + y/freq:.4f} = "
                      f"{r.modified:.4f}.\n4. DV01 = D_mod x P/100 x face x 0.0001 = {fmt_ccy(face / 100 * r.dv01)}.")
    q.facts = {**g, "price": r.price, "macaulay": r.macaulay}
    return q


def s1_l3_big_move(rng, lvl, seed):
    m = int(rng.choice([20, 30])); cpn = 0.04; y = 0.04; bp = float(rng.choice([150, 200, -150, -200])); face = 100e6
    info = bond_info(cpn, m, y)
    g = {"face": face, "coupon_pct": 4.0, "maturity": m, "yield_pct": 4.0, "freq": 2, "price": round(info["price"], 4),
         "dmod": round(info["dmod"], 4), "convexity": round(info["convexity"], 3), "dy_bp": bp}
    labels = {"face": "Face (GBP)", "coupon_pct": "Coupon (%)", "maturity": "Maturity (years)", "yield_pct": "Yield (%)",
              "freq": "Coupons per year", "price": "Price (per 100)", "dmod": "Modified duration",
              "convexity": "Convexity", "dy_bp": "Yield move (bp)"}

    def solver(gv):
        from engine.rates import bond_price
        d, c = approx_pnl(gv["face"], gv["price"], gv["dmod"], gv["convexity"], gv["dy_bp"])
        p0 = bond_price(gv["yield_pct"] / 100, gv["coupon_pct"] / 100, gv["maturity"], int(gv["freq"]))
        p1 = bond_price(gv["yield_pct"] / 100 + gv["dy_bp"] * 1e-4, gv["coupon_pct"] / 100, gv["maturity"], int(gv["freq"]))
        return [(d + c) / 1e3, gv["face"] / 100 * (p1 - p0) / 1e3]
    q = Q("2A-1", "convexity:approx_vs_exact", lvl, "s1_l3_big_move", seed,
          f"You own GBP 100m of a 4% {m}Y gilt and yields move {bp:+.0f}bp. Give (a) the duration+convexity "
          f"approximation and (b) the exact repriced P&L. Which is closer to the truth, and why do they differ?",
          [num("(a) Approximation (GBP k)", "k", tol_rel=0.01, tol_abs=2), num("(b) Exact (GBP k)", "k", tol_rel=0.01, tol_abs=2)],
          "Explain the gap.", "", ["Approximation from D and C", "Exact by repricing", "Gap = higher-order terms, larger for big moves"])
    attach_givens(q, g, labels, solver)
    d, c = approx_pnl(face, g["price"], g["dmod"], g["convexity"], bp)
    q.model_answer = f"**(a) {fmt_ccy(d + c)}, (b) {fmt_ccy(q.parts[1].correct * 1e3)}.**\n\n" + \
        approx_vs_exact_text(d, c, q.parts[1].correct * 1e3)
    q.facts = dict(g)
    return q


# =============================================================================
# Stage 2: bond futures and repo
# =============================================================================
def s2_l1_futures(rng, lvl, seed):
    n = int(rng.choice([1, -1])); bp = float(rng.choice([10, 25]) * rng.choice([1, -1]))
    gains = (n > 0) == (bp < 0)
    return Q("2A-2", "duration:futures", lvl, "s2_l1_futures", seed,
             f"You are **{'long' if n > 0 else 'short'} Long Gilt futures**. Long or short duration? Do you gain or lose if "
             f"yields {'fall' if bp < 0 else 'rise'} {abs(bp):.0f}bp?",
             [mcq("Duration", LONG_SHORT, 0 if n > 0 else 1), mcq("P&L", GAIN_LOSE, 0 if gains else 1)],
             "Explain the link to the cheapest-to-deliver bond.",
             f"**{'Long' if n > 0 else 'Short'} duration; you {'gain' if gains else 'lose'}.**\n\n1. A bond future tracks the "
             f"cheapest-to-deliver bond (scaled by its conversion factor), so long futures behave like a long bond with no cash "
             f"outlay: leveraged duration.\n2. Its DV01 is about the CTD's DV01 divided by the CF.",
             ["Long futures = long duration", "Tracks the CTD / CF"])


def s2_l1_repo(rng, lvl, seed):
    cpn = float(rng.choice([0.04, 0.045, 0.05])); repo = float(rng.choice([0.035, 0.0375, 0.05, 0.055]))
    pos = cpn > repo
    return Q("2A-2", "duration:repo_carry", lvl, "s2_l1_repo", seed,
             f"You buy a gilt trading close to par with a {cpn*100:.2f}% coupon and fund it in repo at {repo*100:.2f}%. "
             f"Is your carry positive or negative? Are you still long duration?",
             [mcq("Carry", ["Positive", "Negative"], 0 if pos else 1), mcq("Duration", LONG_SHORT, 0)],
             "Explain.",
             f"**{'Positive' if pos else 'Negative'} carry; still long duration.**\n\n1. Carry = coupon income minus the "
             f"repo cost of the cash you borrowed. Near par, that is roughly coupon {'>' if pos else '<'} repo rate.\n"
             f"2. Funding in repo changes the cash you put up, not the rate risk: you still own the bond's duration. "
             f"Carry is to bonds what theta is to options.", ["Carry ~ coupon - repo near par", "Still long duration"])


def s2_l2_carry(rng, lvl, seed):
    c = base_curve(); m = int(rng.choice([5, 10, 30])); cpn = float(rng.choice([0.0425, 0.045, 0.0475]))
    face = 100e6; P = Bond(cpn, m, face).pv(c) / face * 100
    repo = float(rng.choice([0.035, 0.0375, 0.04, 0.045, 0.05])); h = 0.25
    g = {"face": face, "coupon_pct": cpn * 100, "dirty_price": round(P, 3), "repo_pct": repo * 100, "horizon_years": h}
    labels = {"face": "Face (GBP)", "coupon_pct": "Coupon (% a year)", "dirty_price": "Dirty price (per 100)",
              "repo_pct": "Repo rate (% a year)", "horizon_years": "Horizon (years)"}
    solver = lambda gv: [(gv["coupon_pct"] / 100 * gv["face"] * gv["horizon_years"]
                          - gv["dirty_price"] / 100 * gv["face"] * gv["repo_pct"] / 100 * gv["horizon_years"]) / 1e3]
    q = Q("2A-2", "duration:repo_carry", lvl, "s2_l2_carry", seed,
          f"You buy GBP 100m of a {cpn*100:.2f}% {m}Y gilt and fund it in 3-month repo. Using the Givens, what is your "
          f"carry over 3 months (ignore pull-to-par)? Are you still long duration?",
          [num("Carry (GBP thousands)", "k", tol_rel=0.02, tol_abs=1), mcq("Duration", LONG_SHORT, 0)],
          "Explain the carry and why duration is unchanged.", "", ["Carry = coupon accrual - repo on the dirty price", "Still long duration"])
    attach_givens(q, g, labels, solver)
    car = q.parts[0].correct * 1e3
    q.model_answer = (f"**Carry {fmt_ccy(car)}; still long duration.**\n\n1. Coupon: {cpn*100:.2f}% x 100m x 0.25 = "
                      f"{fmt_ccy(cpn*face*h)}.\n2. Repo: {repo*100:.2f}% x {P:.3f}/100 x 100m x 0.25 = {fmt_ccy(-P/100*face*repo*h)}.\n"
                      f"3. Funding changes the cash outlay, not the rate risk.")
    q.facts = dict(g)
    return q


def s2_l2_futures_pnl(rng, lvl, seed):
    n = int(rng.choice([200, 500, 1000])) * int(rng.choice([1, -1])); dv = float(rng.choice([85, 92, 101]))
    bp = float(rng.choice([5, 10, 20]) * rng.choice([1, -1]))
    g = {"contracts": n, "dv01_per_contract": dv, "dy_bp": bp}
    labels = {"contracts": "Contracts (+ long / - short)", "dv01_per_contract": "DV01 per contract (GBP per bp)",
              "dy_bp": "Yield move (bp)"}
    solver = lambda gv: [-gv["contracts"] * gv["dv01_per_contract"] * gv["dy_bp"] / 1e3]
    q = Q("2A-2", "duration:futures", lvl, "s2_l2_fut_pnl", seed,
          f"You are {'long' if n > 0 else 'short'} {abs(n)} Long Gilt futures. Using the Givens, what is your P&L if "
          f"yields move {bp:+.0f}bp?", [num("P&L (GBP thousands)", "k", tol_rel=0.01, tol_abs=0.5)], "Explain.", "",
          ["P&L ~ -contracts x DV01 x move"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**{fmt_ccy(q.parts[0].correct * 1e3)}.**\n\n P&L ~ -(contracts x DV01) x move = -({n} x {dv}) x "
                      f"{bp:+.0f}. Long futures gain when yields fall.")
    return q


def s2_l3_hedge(rng, lvl, seed):
    face = float(rng.choice([50e6, 100e6, 200e6])); m = int(rng.choice([8, 10, 12]))
    bond_dv = face / 100 * bond_info(0.045, m, 0.04)["dv01_100"]
    ctd_dv = 100e3 / 100 * bond_info(0.0425, 9, 0.04)["dv01_100"]; cf = 1.0185
    g = {"bond_dv01": round(bond_dv, 0), "ctd_dv01_per_100k": round(ctd_dv, 2), "cf": cf}
    labels = {"bond_dv01": "DV01 of your gilt position (GBP per bp)", "ctd_dv01_per_100k": "CTD DV01 per GBP 100k face (GBP per bp)",
              "cf": "CTD conversion factor"}
    solver = lambda gv: [gv["bond_dv01"] / (gv["ctd_dv01_per_100k"] / gv["cf"])]
    q = Q("2A-2", "duration:futures_hedge", lvl, "s2_l3_hedge", seed,
          f"You own GBP {face/1e6:.0f}m of a 4.5% {m}Y gilt and want to hedge its duration with Long Gilt futures. "
          f"How many contracts do you sell? (Givens)", [num("Contracts to sell", "", tol_rel=0.02, tol_abs=2)],
          "Explain the DV01 per contract and what risks remain.", "",
          ["Futures DV01 = CTD DV01 / CF", "Contracts = position DV01 / futures DV01", "Residual: curve, basis, CTD switch"])
    attach_givens(q, g, labels, solver)
    k = q.parts[0].correct
    q.model_answer = (f"**Sell about {k:,.0f} contracts.**\n\n1. A future behaves like CTD/CF, so DV01 per contract = "
                      f"{g['ctd_dv01_per_100k']} / {cf} = {g['ctd_dv01_per_100k']/cf:.2f}.\n2. Contracts = {g['bond_dv01']:,.0f} / "
                      f"{g['ctd_dv01_per_100k']/cf:.2f} = {k:,.0f}.\n3. Left over: curve risk (your bond is not the CTD), "
                      f"basis risk and the CTD switching.")
    return q


# =============================================================================
# Stage 3: swaps
# =============================================================================
def s3_l1_swap(rng, lvl, seed):
    T = int(rng.choice([2, 5, 10, 30])); d = str(rng.choice(["receive", "pay"]))
    bp = float(rng.choice([10, 25, 50]) * rng.choice([1, -1]))
    longd = d == "receive"; gains = longd == (bp < 0)
    return Q("2A-3", "duration:swaps", lvl, "s3_l1_swap", seed,
             f"You **{d} fixed** on a {T}Y SONIA swap. Long or short duration? Do you gain or lose if rates "
             f"{'fall' if bp < 0 else 'rise'} {abs(bp):.0f}bp?",
             [mcq("Duration", LONG_SHORT, 0 if longd else 1), mcq("P&L", GAIN_LOSE, 0 if gains else 1)],
             "Explain with the bond analogy.",
             f"**{'Long' if longd else 'Short'} duration; you {'gain' if gains else 'lose'}.**\n\n1. Receiving fixed = owning a "
             f"fixed-rate bond funded at the floating rate: you gain when rates fall. Paying fixed is the mirror image.\n"
             f"2. The floating leg resets to market, so it carries almost no duration: all the DV01 is in the fixed leg.",
             ["Receive fixed = long duration", "Bond funded at floating analogy"])


def s3_l1_floater(rng, lvl, seed):
    c = base_curve(); T = int(rng.choice([5, 10]))
    rf, rb = risk(FRN(100e6, 0.25, c.fwd(0, 0.25)), c), risk(Bond(par_swap_rate(c, 0, T), T, 100e6, freq=1), c)
    opts = ["The floating-rate note: it has almost no duration", "The fixed-rate bond: it has almost no duration",
            "They have similar duration"]
    return Q("2A-3", "duration:floaters", lvl, "s3_l1_floater", seed,
             f"GBP 100m of a {T}Y SONIA floating-rate note (resets quarterly) vs GBP 100m of a {T}Y fixed bond. Which one "
             f"has almost no duration?", [mcq("Answer", opts, 0)], "Why?",
             f"**The floater.** Its coupon resets to market each period, so after a reset it is worth about par whatever "
             f"rates did; its only rate risk is until the next reset. Illustration: DV01 {fmt_ccy(rf.dv01)} vs "
             f"{fmt_ccy(rb.dv01)}.", ["Floater resets to market", "Duration ~ time to next reset"])


def s3_l1_forward(rng, lvl, seed):
    s, L = [(2, 3), (5, 5), (1, 4)][int(rng.integers(3))]
    opts = [f"Long duration around {s + L}Y, short around {s}Y", f"Long duration at every tenor up to {s + L}Y",
            f"Short duration around {s + L}Y, long around {s}Y", "No duration until the swap starts"]
    return Q("2A-3", "duration:forward_swaps", lvl, "s3_l1_forward", seed,
             f"You receive fixed on a **{s}Y{L}Y forward-starting swap**. Where along the curve is your duration?",
             [mcq("Exposure", opts, 0)], "Explain.",
             f"**{opts[0]}.** A {s}Y{L}Y receiver = receive {s + L}Y and pay {s}Y: the near cash flows cancel, leaving a bet on "
             f"the {s}Y{L}Y forward rate (long the {s + L}Y point, short the {s}Y point).",
             ["Equivalent to long (s+L)Y receiver and short sY receiver"])


def s3_l2_swap_pnl(rng, lvl, seed):
    c = base_curve(); T = int(rng.choice([5, 10])); d = str(rng.choice(["receive", "pay"])); bp = float(rng.choice([25, 50]) * rng.choice([1, -1]))
    sw = Swap(0, T, par_swap_rate(c, 0, T), 100e6, d); r = risk(sw, c)
    g = {"dv01": round(r.dv01, 0), "dy_bp": bp}
    labels = {"dv01": "Position DV01 (GBP per bp, + = long duration)", "dy_bp": "Parallel move (bp)"}
    solver = lambda gv: [-gv["dv01"] * gv["dy_bp"] / 1e3]
    q = Q("2A-3", "duration:swaps", lvl, "s3_l2_swap_pnl", seed,
          f"You {d} fixed on GBP 100m {T}Y SONIA at par. Using the Givens, estimate your P&L if rates move {bp:+.0f}bp.",
          [num("P&L (GBP thousands)", "k", tol_rel=0.01, tol_abs=0.5), mcq("Duration", LONG_SHORT, 0 if d == "receive" else 1)],
          "Explain, and say why the exact P&L differs slightly.", "", ["P&L ~ -DV01 x move", "Convexity of the swap"])
    attach_givens(q, g, labels, solver)
    exact = pnl(sw, c, c.shifted(bp)); est = q.parts[0].correct * 1e3
    q.model_answer = (f"**About {fmt_ccy(est)}.**\n\n(a) First order: -DV01 x move = {fmt_ccy(est)}.\n(b) Exact (engine, curve "
                      f"shifted and repriced): {fmt_ccy(exact)}. Gap {fmt_ccy(exact - est)}: the swap's convexity "
                      f"({'helps' if exact - est > 0 else 'hurts'} here).")
    q.facts = {**g, "exact": exact}
    return q


def s3_l3_annuity(rng, lvl, seed):
    c = base_curve(); s = int(rng.choice([2, 5])); L = int(rng.choice([3, 5])); N = 100e6
    from engine.rates import annuity
    A_end, A_start = annuity(c, 0, s + L), annuity(c, 0, s)
    g = {"notional": N, "annuity_0_to_end": round(A_end, 5), "annuity_0_to_start": round(A_start, 5)}
    labels = {"notional": "Notional (GBP)", "annuity_0_to_end": f"Annuity factor, 0 to {s + L}Y (sum of DF x accrual)",
              "annuity_0_to_start": f"Annuity factor, 0 to {s}Y"}
    solver = lambda gv: [gv["notional"] * gv["annuity_0_to_end"] * 1e-4, gv["notional"] * (gv["annuity_0_to_end"] - gv["annuity_0_to_start"]) * 1e-4]
    q = Q("2A-3", "duration:swap_dv01", lvl, "s3_l3_annuity", seed,
          f"Using the annuity factors in the Givens, compute (a) the DV01 of receiving fixed on GBP 100m {s + L}Y spot-start, "
          f"and (b) the DV01 of receiving fixed on GBP 100m {s}Y{L}Y forward-start.",
          [num(f"(a) {s + L}Y DV01 (GBP per bp)", tol_rel=0.01), num(f"(b) {s}Y{L}Y DV01 (GBP per bp)", tol_rel=0.01)],
          "Explain why the forward swap's DV01 is the difference.", "",
          ["DV01 ~ notional x annuity x 1bp", "Forward swap = long the long swap, short the short swap"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**(a) {fmt_ccy(q.parts[0].correct)}, (b) {fmt_ccy(q.parts[1].correct)} per bp.**\n\n1. A 1bp change in "
                      f"the fixed rate changes the fixed leg's PV by notional x annuity x 0.0001.\n2. The forward swap's "
                      f"fixed payments run from {s}Y to {s + L}Y, so its annuity = A(0,{s + L}) - A(0,{s}).\n3. This is "
                      f"the par-rate DV01; a zero-curve bump gives a very similar number.")
    return q


# =============================================================================
# Stage 4: swaptions
# =============================================================================
def _swpt(c, kind, side, exp=1.0, ten=10.0, n=100e6, off=0.0):
    return Swaption(exp, ten, par_swap_rate(c, exp, exp + ten) + off * 1e-4, NVOL, kind, side * n)


def s4_l1_signs(rng, lvl, seed):
    c = base_curve(); kind = str(rng.choice(["payer", "receiver"])); side = int(rng.choice([1, -1]))
    r = risk(_swpt(c, kind, side), c); ref = risk(_swpt(c, "receiver", 1), c)
    corr = {"Duration": sign_word(r.dv01, ref.dv01), "Convexity": sign_word(r.convexity_pnl, ref.convexity_pnl)}
    from grading.question import Part
    return Q("2A-4", "convexity:swaptions", lvl, "s4_l1_signs", seed,
             f"You are **{'long' if side > 0 else 'short'} 1Y-into-10Y ATM {kind} swaptions**. Fill in your exposures "
             f"(+ long, - short).",
             [Part("sign_table", "Exposure", rows=["Duration", "Convexity"], correct=corr)], "Explain each sign.",
             f"**Duration {corr['Duration']}, convexity {corr['Convexity']}.**\n\n1. Receiver = right to receive fixed: gains "
             f"when rates fall, so long duration. Payer = short duration.\n2. Any long option is long convexity (long gamma): "
             f"its duration grows in the direction that makes money. Short either one and you are short convexity.",
             ["Receiver long duration / payer short", "Long option = long convexity; short = short convexity"],
             charts=[_pnl_chart(_swpt(c, kind, side), c, "Swaption P&L vs parallel move")])


def s4_l2_delta(rng, lvl, seed):
    c = base_curve(); kind = str(rng.choice(["payer", "receiver"])); side = int(rng.choice([1, -1]))
    bp = float(rng.choice([25, 50, 75]) * rng.choice([1, -1])); sw = _swpt(c, kind, side)
    r0, r1 = risk(sw, c), risk(sw, c.shifted(bp)); grew = abs(r1.dv01) > abs(r0.dv01)
    hedged = rng.random() < 0.5
    if hedged:
        prompt = (f"You are **{'long' if side > 0 else 'short'} 1Y10Y ATM {kind} swaptions, delta-hedged with swaps** "
                  f"(flat duration today). Rates move {bp:+.0f}bp. Are you now long or short duration?")
        net = r1.dv01 - r0.dv01
        parts = [mcq("Duration after the move", LONG_SHORT, 0 if net > 0 else 1)]
        ans = f"**{'Long' if net > 0 else 'Short'} duration** (net DV01 {fmt_ccy(net)})."
    else:
        prompt = (f"You are **{'long' if side > 0 else 'short'} 1Y10Y ATM {kind} swaptions**. Rates move {bp:+.0f}bp. "
                  f"Does the size of your duration exposure grow or shrink?")
        parts = [mcq("Duration exposure", ["Grows", "Shrinks"], 0 if grew else 1)]
        ans = f"**It {'grows' if grew else 'shrinks'}: DV01 {fmt_ccy(r0.dv01)} to {fmt_ccy(r1.dv01)}.**"
    return Q("2A-4", "convexity:swaption_delta", lvl, "s4_l2_delta", seed, prompt, parts, "Explain using the option analogy.",
             ans + "\n\n1. A swaption's DV01 behaves like an option delta: it grows as the option moves into the money.\n"
             f"2. {'Long the option, your duration always moves in your favour (long convexity): after a hedge you end up long duration in a rally and short in a selloff.' if side > 0 else 'Short the option, your duration moves against you (short convexity): you end up long duration in a selloff and short in a rally.'}",
             ["Swaption delta changes like option delta", "Long vs short convexity"])


def s4_l3_bachelier(rng, lvl, seed):
    c = base_curve(); kind = str(rng.choice(["payer", "receiver"])); off = float(rng.choice([-25, 0, 25]))
    from engine.rates import annuity
    F = par_swap_rate(c, 1, 11); A = annuity(c, 1, 11)
    g = {"type": kind, "F_pct": round(F * 100, 4), "K_pct": round((F + off * 1e-4) * 100, 4), "normal_vol_bp": NVOL * 1e4,
         "T": 1.0, "annuity": round(A, 5), "notional": 100e6}
    labels = {"type": "Swaption type (you are long)", "F_pct": "Forward swap rate (%)", "K_pct": "Strike (%)", "normal_vol_bp": "Normal vol (bp a year)",
              "T": "Expiry (years)", "annuity": "Forward annuity factor", "notional": "Notional (GBP)"}

    def solver(gv):
        F_, K_ = gv["F_pct"] / 100, gv["K_pct"] / 100
        sd = gv["normal_vol_bp"] * 1e-4 * math.sqrt(gv["T"])
        d = (F_ - K_) / sd
        Nd = 0.5 * (1 + math.erf(d / math.sqrt(2))); nd = math.exp(-0.5 * d * d) / math.sqrt(2 * math.pi)
        if gv["type"] == "payer":
            pv = gv["annuity"] * ((F_ - K_) * Nd + sd * nd); dv01 = -gv["annuity"] * Nd * 1e-4
        else:
            pv = gv["annuity"] * ((K_ - F_) * (1 - Nd) + sd * nd); dv01 = gv["annuity"] * (1 - Nd) * 1e-4
        return [pv * gv["notional"] / 1e3, dv01 * gv["notional"]]
    q = Q("2A-4", "convexity:swaption_pricing", lvl, "s4_l3_bachelier", seed,
          f"Price a long GBP 100m 1Y-into-10Y **{kind}** swaption ({'ATM' if off == 0 else f'{off:+.0f}bp from ATM'}) under "
          f"Bachelier (normal) vol, and give its DV01 (+ = long duration). All inputs in the Givens.",
          [num("Premium (GBP thousands)", "k", tol_rel=0.02), num("DV01 (GBP per bp)", tol_rel=0.03)],
          "Explain the formula and the sign of the DV01.", "",
          ["PV = A [(F-K) N(d) + sigma sqrt(T) n(d)] for a payer", "DV01 = -A N(d) x 1bp (payer)"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**Premium {fmt_ccy(q.parts[0].correct * 1e3)}, DV01 {fmt_ccy(q.parts[1].correct)}.**\n\n"
                      f"1. d = (F - K) / (sigma_N sqrt T); payer PV = A [(F-K) N(d) + sigma_N sqrt(T) n(d)], receiver PV = "
                      f"A [(K-F) N(-d) + sigma_N sqrt(T) n(d)].\n2. Delta to the forward rate: payer A N(d), receiver -A N(-d); "
                      f"DV01 (long duration +) = -delta x 1bp, so payers are short duration.\n3. ATM: PV = A sigma_N sqrt(T/2pi).")
    return q


# =============================================================================
# Stage 5: mixed books
# =============================================================================
def _book(c, rng):
    v = str(rng.choice(["rec_plus_payer", "bond_short_receiver", "callable", "payer_hedged", "mbs_hedged"]))
    if v == "rec_plus_payer":
        sw = Swap(0, 10, par_swap_rate(c, 0, 10), 100e6, "receive"); opt = _swpt(c, "payer", 1, 2.0, 10.0, float(rng.choice([50e6, 100e6])))
        return v, Composite([sw, opt]), (f"The desk **receives fixed on GBP 100m 10Y** and is **long GBP {opt.notional/1e6:.0f}m "
                                        f"2Y-into-10Y ATM payer swaptions**.")
    if v == "bond_short_receiver":
        return v, Composite([Bond(0.045, 10, 100e6), _swpt(c, "receiver", -1, 1.0, 9.0, 100e6, -25)]), \
            "The desk owns **GBP 100m of a 4.5% 10Y gilt** and has **sold GBP 100m 1Y-into-9Y receiver swaptions** 25bp OTM."
    if v == "callable":
        return v, callable_bond(0.045, 10, 2, 100e6, NVOL, c), \
            "The desk owns **GBP 100m of a 4.5% 10Y callable bond** (callable at par in 2 years), MBS-like."
    if v == "mbs_hedged":
        cb = callable_bond(0.045, 10, 2, 100e6, NVOL, c); d = risk(cb, c).dv01
        sw = Swap(0, 10, par_swap_rate(c, 0, 10), d / risk(Swap(0, 10, par_swap_rate(c, 0, 10), 1.0), c).dv01, "pay")
        return v, Composite([cb, sw]), "The desk owns **GBP 100m of an MBS-like 4.5% 10Y callable bond, duration-hedged by paying fixed in 10Y swaps**."
    opt = _swpt(c, "payer", 1); d = risk(opt, c).dv01
    sw = Swap(0, 10, par_swap_rate(c, 0, 10), abs(d) / risk(Swap(0, 10, par_swap_rate(c, 0, 10), 1.0), c).dv01, "receive")
    return v, Composite([opt, sw]), "The desk is **long GBP 100m 1Y-into-10Y ATM payer swaptions, delta-hedged by receiving 10Y**."


LOGIC = {
    "rec_plus_payer": "Receiving 10Y is long duration with little convexity; the long payers are short duration and long convexity. In a selloff the payers' delta grows and offsets more of the swap loss.",
    "bond_short_receiver": "Selling receivers adds long duration that grows as rates fall and vanishes as they rise: short convexity, paid for with premium. Same shape as a callable bond or MBS.",
    "callable": "A callable bond = bullet bond minus the issuer's call (a receiver swaption you are short). When rates fall it gets called, so duration shortens just when you want more: long duration, short convexity.",
    "mbs_hedged": "Duration-hedged MBS is flat duration today but short convexity: after a rally you are short duration, after a selloff long. Hedgers chase the move (convexity hedging).",
    "payer_hedged": "A delta-hedged long payer is flat duration but long convexity: after a selloff you are short duration (you made money), after a rally long. Long gamma in rates.",
}


def s5_l1_signs(rng, lvl, seed):
    c = base_curve(); v, book, desc = _book(c, rng); r = risk(book, c)
    ref_d = 100e6 * 1e-4 * 4; ref_c = risk(_swpt(c, "receiver", 1), c).convexity_pnl
    corr = {"Duration": sign_word(r.dv01, ref_d, 0.1), "Convexity": sign_word(r.convexity_pnl, ref_c, 0.1)}
    from grading.question import Part
    return Q("2A-5", "mixed:signs", lvl, "s5_l1_signs", seed, desc + "\n\nFill in the book's exposures today (+ long, - short, 0 roughly flat).",
             [Part("sign_table", "Exposure", rows=["Duration", "Convexity"], correct=corr)], "Explain.",
             f"**Duration {corr['Duration']}, convexity {corr['Convexity']}.**\n\n{LOGIC[v]}", [LOGIC[v]], {"variant": v})


def s5_l2_move(rng, lvl, seed):
    c = base_curve(); v, book, desc = _book(c, rng); bp = float(rng.choice([50, 75, -50, -75]))
    p = pnl(book, c, c.shifted(bp)); r0, r1 = risk(book, c), risk(book, c.shifted(bp))
    ref_c = risk(_swpt(c, "receiver", 1), c).convexity_pnl
    corr = {"P&L": "+" if p > 0 else "-", "Duration after": sign_word(r1.dv01, 100e6 * 1e-4 * 4, 0.05),
            "Convexity after": sign_word(r1.convexity_pnl, ref_c, 0.1)}
    from grading.question import Part
    return Q("2A-5", "mixed:books", lvl, "s5_l2_move", seed,
             desc + f"\n\nRates move **{bp:+.0f}bp** in parallel. Fill in the sign of your P&L and of your exposures after "
             f"the move, then walk through why.",
             [Part("sign_table", "After the move", rows=list(corr), correct=corr)], "Walk through the P&L by component and the change in risk.",
             f"**P&L {corr['P&L']}, duration {corr['Duration after']}, convexity {corr['Convexity after']}.**\n\n{LOGIC[v]}\n\n"
             f"Illustration (engine): P&L {fmt_ccy(p)}; DV01 {fmt_ccy(r0.dv01)} to {fmt_ccy(r1.dv01)}.",
             [LOGIC[v], "P&L sign by component"], {"variant": v, "pnl": p},
             charts=[_pnl_chart(book, c, "Book P&L vs parallel move")])


def s5_l3_taylor(rng, lvl, seed):
    c = base_curve(); v, book, desc = _book(c, rng); bp = float(rng.choice([50, -50, 75, -75]))
    g = {}
    labels = {}
    for i, part in enumerate(book.parts):
        nm = getattr(part, "name", f"leg{i}")
        g[f"dv01_{i}"] = round(risk(part, c).dv01, 0); labels[f"dv01_{i}"] = f"{nm}: DV01 (GBP/bp, + long duration)"
        g[f"gamma_{i}"] = round(dv01_gamma(part, c), 2); labels[f"gamma_{i}"] = f"{nm}: change in DV01 per +1bp (GBP/bp per bp)"
    g["dy_bp"] = bp; labels["dy_bp"] = "Parallel move (bp)"
    def solver(gv):
        legs = sorted(int(k.split("_")[1]) for k in gv if k.startswith("dv01_"))
        return [sum(-gv[f"dv01_{i}"] * gv["dy_bp"] - 0.5 * gv[f"gamma_{i}"] * gv["dy_bp"] ** 2 for i in legs) / 1e3]
    q = Q("2A-5", "mixed:books_sized", lvl, "s5_l3_taylor", seed,
          desc + f"\n\nRates move **{bp:+.0f}bp**. Using the DV01s and gammas in the Givens, estimate the book's P&L. Then explain "
          f"how the risk has changed.", [num("P&L (GBP thousands)", "k", tol_rel=0.03, tol_abs=2)],
          "Walk through the P&L and the change in risk.", "",
          ["P&L ~ sum(-DV01 dy - 0.5 G dy^2)", LOGIC[v]])
    attach_givens(q, g, labels, solver)
    exact = pnl(book, c, c.shifted(bp)); est = q.parts[0].correct * 1e3
    q.model_answer = (f"**About {fmt_ccy(est)}.**\n\n1. Each leg: P&L ~ -DV01 x dy - 0.5 x G x dy^2, where G is how much the "
                      f"DV01 changes per +1bp (negative for long convexity).\n2. Exact (engine, repriced): {fmt_ccy(exact)}; "
                      f"gap {fmt_ccy(exact - est)} from higher-order option terms.\n3. {LOGIC[v]}")
    q.facts = {**g, "exact": exact}
    return q


STAGES = {
    "2A-1": ("Stage 1: Government bonds", {1: [s1_l1_position, s1_l1_compare, s1_l1_asymmetry],
                                            2: [s1_l2_sized, s1_l2_asymmetry_sized], 3: [s1_l3_compute, s1_l3_big_move]}),
    "2A-2": ("Stage 2: Bond futures and repo", {1: [s2_l1_futures, s2_l1_repo], 2: [s2_l2_carry, s2_l2_futures_pnl],
                                                 3: [s2_l3_hedge]}),
    "2A-3": ("Stage 3: Swaps", {1: [s3_l1_swap, s3_l1_floater, s3_l1_forward], 2: [s3_l2_swap_pnl], 3: [s3_l3_annuity]}),
    "2A-4": ("Stage 4: Swaptions", {1: [s4_l1_signs], 2: [s4_l2_delta], 3: [s4_l3_bachelier]}),
    "2A-5": ("Stage 5: Mixed books", {1: [s5_l1_signs], 2: [s5_l2_move], 3: [s5_l3_taylor]}),
}


def make_generator(stage: str):
    levels = STAGES[stage][1]

    def gen(seed: int, difficulty: int):
        rng = np.random.default_rng(seed)
        fns = levels[difficulty]
        return fns[int(rng.integers(len(fns)))](rng, difficulty, seed)
    return gen

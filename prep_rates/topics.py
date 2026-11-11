"""Sections 2B-2F, each tiered:
L1 intuition only, L2 light calculations with full Givens, L3 multi-step / advanced with full Givens."""
from __future__ import annotations

import numpy as np

from engine.config import load_config
from engine.rates import annuity, bond_risk, ctd_analysis, key_rate_dv01s, par_swap_rate
from grading.question import attach_givens, chart_bar
from prep_rates.instruments import (Bond, Composite, Swap, Swaption, ZeroCurve, base_curve, fmt_ccy,
                                    move_curve, pnl, risk)
from prep_rates.qkit import GAIN_LOSE, LONG_SHORT, Q, dv01_gamma, mcq, num, shuffle_opts

CFG = load_config()["rates_engine"]
NVOL = CFG["swaption_normal_vol_bp"] / 1e4


# =============================================================================
# 2B Convexity
# =============================================================================
def _barbell(c):
    bullet = Bond(0.0, 10, 100e6)
    rb = risk(bullet, c)
    s, l = Bond(0.0, 2, 1.0), Bond(0.0, 30, 1.0)
    A = np.array([[s.pv(c), l.pv(c)], [risk(s, c).dv01, risk(l, c).dv01]])
    w = np.linalg.solve(A, np.array([rb.pv, rb.dv01]))
    return bullet, Composite([Bond(0.0, 2, w[0]), Bond(0.0, 30, w[1])]), w


def b_l1_barbell(rng, lvl, seed):
    opts = ["The barbell, in either direction", "The bullet, in either direction", "The barbell only if yields fall"]
    return Q("2B", "convexity:barbell", lvl, "b_l1_barbell", seed,
             "A 10Y zero (bullet) vs a 2Y/30Y zero barbell with the **same PV and DV01**. Yields jump 100bp, up or down. "
             "Which does better? What do you give up for that?",
             [mcq("Better in a big parallel move", opts, 0)], "Explain, including the cost.",
             "**The barbell, both ways.**\n\n1. Same duration, but the barbell's cash flows are spread out, and convexity "
             "grows roughly with maturity squared: the 30Y wing adds far more convexity than the 2Y wing loses.\n"
             "2. You pay for it: lower yield/carry in a fair market, and the barbell is SHORT the belly vs the wings, so it "
             "loses if the 10Y richens relative to 2Y and 30Y.\n3. Same trade-off as gamma vs theta.",
             ["Barbell has more convexity", "Costs yield/carry", "Exposed to belly vs wings"])


def b_l1_mortgage(rng, lvl, seed):
    opts, corr = shuffle_opts(rng, "Receive fixed / buy duration, pushing yields lower still",
                              ["Pay fixed / sell duration, pushing yields back up", "Nothing: MBS duration does not depend on rates"])
    return Q("2B", "convexity:mortgage", lvl, "b_l1_mbs", seed,
             "Rates rally hard. What do MBS holders who hedge their duration do, and what does it do to the market?",
             [mcq("Hedging flow", opts, corr)], "Explain the chain.",
             "**They buy duration.** MBS holders are short the borrowers' prepayment option: as rates fall, borrowers "
             "refinance, the MBS shortens (negative convexity), so hedgers must receive fixed or buy long bonds to get "
             "duration back. That flow chases the move and amplifies it.",
             ["Prepayments shorten duration in a rally", "Hedgers buy duration", "Amplifies the move"])


def b_l1_cost(rng, lvl, seed):
    opts, corr = shuffle_opts(rng, "Premium or lower yield/carry: you pay for convexity like you pay theta for gamma",
                              ["Nothing: convexity is free", "Higher duration", "Higher credit risk"])
    return Q("2B", "convexity:cost", lvl, "b_l1_cost", seed,
             "You add long convexity to a rates book (buy a swaption straddle, or swap a bullet for a barbell). What do you "
             "pay for it?", [mcq("Cost", opts, corr)], "Explain the analogy with options.",
             "**You pay premium or give up yield.** Long convexity gains from big moves either way, so the market charges "
             "for it: option premium decays (theta), or the higher-convexity bond yields less. If rates sit still, you bleed.",
             ["Convexity has a cost", "Gamma/theta analogy"])


def b_l2_maturity(rng, lvl, seed):
    t1, t2 = [(5, 10), (5, 20), (10, 30), (2, 10)][int(rng.integers(4))]
    y = 0.04
    g = {"T1": t1, "T2": t2, "y_pct": 4.0}
    labels = {"T1": "Maturity of zero A (years)", "T2": "Maturity of zero B (years)", "y_pct": "Yield (%, annual comp.)"}
    solver = lambda gv: [(gv["T2"] * (gv["T2"] + 1)) / (gv["T1"] * (gv["T1"] + 1))]
    q = Q("2B", "convexity:maturity", lvl, "b_l2_maturity", seed,
          f"For an annual zero, convexity = T(T+1)/(1+y)^2. How many times more convexity does the {t2}Y zero have than "
          f"the {t1}Y zero?", [num("Ratio", "x", tol_rel=0.02)], "Explain the scaling.", "",
          ["Convexity ~ T^2", "The (1+y)^2 cancels in the ratio"])
    attach_givens(q, g, labels, solver)
    r = q.parts[0].correct
    q.model_answer = (f"**{r:.2f}x.** The (1+y)^2 terms cancel: {t2}x{t2+1} / ({t1}x{t1+1}) = {r:.2f}. Engine check: "
                      f"{bond_risk(y, 0, t2, 1).convexity:.1f} vs {bond_risk(y, 0, t1, 1).convexity:.1f}. Convexity lives at the long end.")
    return q


def b_l2_barbell(rng, lvl, seed):
    c = base_curve(); bullet, bar, w = _barbell(c); bp = int(rng.choice([75, 100, 150]))
    pv = bullet.pv(c)
    cb = 0.5 * (pnl(bullet, c, c.shifted(25)) + pnl(bullet, c, c.shifted(-25))) / (pv * (25e-4) ** 2)
    cbar = 0.5 * (pnl(bar, c, c.shifted(25)) + pnl(bar, c, c.shifted(-25))) / (pv * (25e-4) ** 2)
    g = {"pv": round(pv, 0), "convexity_bullet": round(2 * cb, 2), "convexity_barbell": round(2 * cbar, 2), "dy_bp": bp}
    labels = {"pv": "PV of each portfolio (GBP)", "convexity_bullet": "Bullet convexity (years^2)",
              "convexity_barbell": "Barbell convexity (years^2)", "dy_bp": "Parallel move (bp, either way)"}
    solver = lambda gv: [0.5 * (gv["convexity_barbell"] - gv["convexity_bullet"]) * gv["pv"] * (gv["dy_bp"] * 1e-4) ** 2 / 1e3]
    q = Q("2B", "convexity:barbell", lvl, "b_l2_barbell", seed,
          f"Bullet vs barbell with the same PV and duration (Givens). Estimate how much more the barbell makes than the "
          f"bullet if yields move {bp}bp in either direction.", [num("Barbell minus bullet (GBP k)", "k", tol_rel=0.05, tol_abs=2)],
          "What do you give up for it?", "", ["Duration terms cancel", "0.5 (C_bar - C_bul) PV dy^2", "Costs yield / curve risk"])
    attach_givens(q, g, labels, solver)
    exact = pnl(bar, c, c.shifted(-bp)) - pnl(bullet, c, c.shifted(-bp))
    q.model_answer = (f"**About {fmt_ccy(q.parts[0].correct * 1e3)}.**\n\n1. Equal duration, so the duration terms cancel; "
                      f"only convexity is left: 0.5 x (C_barbell - C_bullet) x PV x dy^2.\n2. Exact (engine, -{bp}bp): "
                      f"{fmt_ccy(exact)}.\n3. The cost: lower yield, and exposure to the belly richening vs the wings.")
    return q


def b_l3_straddle(rng, lvl, seed):
    c = base_curve(); F = par_swap_rate(c, 1, 11)
    st = Composite([Swaption(1, 10, F, NVOL, "payer", 100e6), Swaption(1, 10, F, NVOL, "receiver", 100e6)])
    rv = float(rng.choice([55, 65, 75, 95, 110]))
    g = {"premium": round(st.pv(c), 0), "annuity_pv_per_bp": round(annuity(c, 1, 11) * 100e6 * 1e-4, 0),
         "realised_vol_bp": rv}
    labels = {"premium": "Straddle premium (GBP)", "annuity_pv_per_bp": "Forward annuity PV per bp (GBP)",
              "realised_vol_bp": "Realised normal vol of the forward rate over the year (bp)"}
    solver = lambda gv: [gv["premium"] / gv["annuity_pv_per_bp"],
                         (0.7979 * gv["realised_vol_bp"] * gv["annuity_pv_per_bp"] - gv["premium"]) / 1e3]
    q = Q("2B", "convexity:cost", lvl, "b_l3_straddle", seed,
          f"You buy GBP 100m of a 1Y-into-10Y ATM swaption straddle (implied normal vol {NVOL*1e4:.0f}bp). (a) How far must "
          f"the forward swap rate move by expiry, either way, to break even? (b) If the rate's realised normal vol over the "
          f"year turns out to be {rv:.0f}bp, what is your expected P&L at expiry? (E|move| = sigma x sqrt(2/pi).)",
          [num("(a) Breakeven (bp)", "bp", tol_rel=0.03), num("(b) Expected P&L (GBP k)", "k", tol_rel=0.05, tol_abs=20)],
          "How is this like gamma vs theta?", "",
          ["Breakeven = premium / annuity per bp", "Expected payoff = annuity x sigma_realised x sqrt(2/pi)",
           "Long convexity wins only if realised beats implied"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**(a) {q.parts[0].correct:.0f}bp, (b) {fmt_ccy(q.parts[1].correct * 1e3)}.**\n\n1. At expiry the "
                      f"straddle pays annuity x |move|, so breakeven = premium / (annuity PV per bp).\n2. Expected payoff = "
                      f"annuity x E|move| = annuity x {rv:.0f} x 0.798 = {fmt_ccy(0.7979 * rv * g['annuity_pv_per_bp'])}; minus "
                      f"the premium gives (b).\n3. For an ATM straddle the breakeven equals E|move| at the IMPLIED vol "
                      f"({NVOL*1e4:.0f}bp x 0.798), so you make money exactly when realised beats implied: pure long "
                      f"convexity, paid for up front (theta).")
    return q


# =============================================================================
# 2C Curve trades
# =============================================================================
LABELS = ["Bull steepener", "Bull flattener", "Bear steepener", "Bear flattener"]
DRIVERS = {
    "Bull steepener": "front end rallies more: earlier or deeper central-bank cuts priced",
    "Bull flattener": "long end rallies more: growth/inflation fears, flight to duration, long-end demand",
    "Bear steepener": "long end sells off more: term premium, supply, fiscal or inflation worries",
    "Bear flattener": "front end sells off more: hikes, or cuts priced out",
}


def _moves(rng, lab):
    a, b = sorted([float(rng.integers(5, 15)), float(rng.integers(20, 40))])
    bull, steep = lab.startswith("Bull"), lab.endswith("steepener")
    if bull:
        return (-b, -a) if steep else (-a, -b)
    return (a, b) if steep else (b, a)


def _steepener(c, n10=100e6):
    p2, p10 = par_swap_rate(c, 0, 2), par_swap_rate(c, 0, 10)
    pay10 = Swap(0, 10, p10, n10, "pay")
    d10 = abs(risk(pay10, c).dv01); d2u = risk(Swap(0, 2, p2, 1.0, "receive"), c).dv01
    return Swap(0, 2, p2, d10 / d2u, "receive"), pay10


def c_l1_label(rng, lvl, seed):
    lab = str(rng.choice(LABELS)); m2, m10 = _moves(rng, lab)
    makes = (m10 - m2) > 0
    return Q("2C", "curve:labels", lvl, "c_l1_label", seed,
             f"2Y SONIA swaps move **{m2:+.0f}bp** and 10Y move **{m10:+.0f}bp**. What kind of move is this? Does a "
             f"DV01-neutral 2s10s steepener make or lose money?",
             [mcq("Curve move", LABELS, LABELS.index(lab)), mcq("Steepener", ["Makes money", "Loses money"], 0 if makes else 1)],
             "What typically drives this kind of move?",
             f"**{lab}; the steepener {'makes' if makes else 'loses'} money.**\n\n1. Bull = yields fall, bear = yields rise; "
             f"steepener = 10Y minus 2Y widens.\n2. The curve {'steepened' if makes else 'flattened'} by {abs(m10 - m2):.0f}bp. "
             f"A DV01-neutral steepener (receive 2Y, pay 10Y) earns DV01 x (change in 10Y - change in 2Y).\n"
             f"3. Typical driver: {DRIVERS[lab]}.", [lab, DRIVERS[lab]])


def c_l1_convexity(rng, lvl, seed):
    trade = str(rng.choice(["steepener", "flattener"]))
    q_kind = str(rng.choice(["sign", "big_move"]))
    c = base_curve(); rec2, pay10 = _steepener(c)
    book = Composite([rec2, pay10]) if trade == "steepener" else Composite([
        Swap(0, 2, rec2.fixed, rec2.notional, "pay"), Swap(0, 10, pay10.fixed, pay10.notional, "receive")])
    cx = risk(book, c).convexity_pnl
    if q_kind == "sign":
        prompt = f"You hold a **DV01-neutral 2s10s {trade}**. Are you long or short convexity, and why?"
        parts = [mcq("Convexity", LONG_SHORT, 0 if cx > 0 else 1)]
    else:
        bp = int(rng.choice([75, 100])) * int(rng.choice([1, -1]))
        p = pnl(book, c, c.shifted(bp))
        prompt = (f"You hold a **DV01-neutral 2s10s {trade}**. The whole curve moves {bp:+d}bp in parallel (no change in "
                  f"slope). Do you make or lose money?")
        parts = [mcq("P&L", GAIN_LOSE, 0 if p > 0 else 1)]
    return Q("2C", "curve:convexity", lvl, f"c_l1_convexity_{q_kind}", seed, prompt, parts,
             "Explain using convexity per unit of DV01, and how it interacts with a bull or bear move.",
             f"**A DV01-neutral steepener is SHORT convexity; a flattener is LONG convexity.**\n\n1. Convexity per unit of "
             f"DV01 rises with maturity, so the 10Y leg carries far more convexity than the 2Y leg for the same DV01.\n"
             f"2. A steepener pays fixed in 10Y (short the 10Y's convexity) and receives 2Y (long a little): net short. Big "
             f"parallel moves either way hurt the steepener and help the flattener, all else equal.\n3. Interaction: in a "
             f"bull steepener the slope gain is partly offset by the convexity loss; in a large bear flattener the "
             f"flattener earns both slope and convexity.\n4. Illustration (engine): +/-25bp convexity P&L of this "
             f"{trade} = {fmt_ccy(cx)}.",
             ["Steepener short convexity, flattener long", "10Y has more convexity per DV01", "Big parallel moves hurt the steepener"])


def c_l1_boe(rng, lvl, seed):
    opts, corr = shuffle_opts(rng, "Receive 2Y vs pay 10Y, DV01-weighted (steepener)",
                              ["Pay 2Y vs receive 10Y (flattener)", "Pay 10Y outright", "Buy 30Y gilts outright"])
    return Q("2C", "curve:expression", lvl, "c_l1_boe", seed,
             "You think the BoE cuts sooner than the market prices. What curve trade expresses it?",
             [mcq("Trade", opts, corr)], "Explain, including the main risks.",
             "**Receive the front end: a DV01-neutral 2s10s steepener.** Earlier cuts pull down expected policy rates over "
             "the next 1-2 years, so the front end rallies most (bull steepener). DV01 weighting removes the bet on the level. "
             "Risks: growth fears rally the long end too (bull flattener), and the steepener is short convexity.",
             ["Receive front end / steepener", "DV01-neutral", "Risks"])


def c_l2_pnl(rng, lvl, seed):
    c = base_curve(); lab = str(rng.choice(LABELS)); m2, m10 = _moves(rng, lab); rec2, pay10 = _steepener(c)
    g = {"dv01_2y_leg": round(risk(rec2, c).dv01, 0), "dv01_10y_leg": round(risk(pay10, c).dv01, 0), "move_2y_bp": m2,
         "move_10y_bp": m10}
    labels = {"dv01_2y_leg": "DV01 of the receive-2Y leg (GBP/bp, + long duration)",
              "dv01_10y_leg": "DV01 of the pay-10Y leg (GBP/bp, - short duration)", "move_2y_bp": "2Y move (bp)",
              "move_10y_bp": "10Y move (bp)"}
    solver = lambda gv: [(-gv["dv01_2y_leg"] * gv["move_2y_bp"] - gv["dv01_10y_leg"] * gv["move_10y_bp"]) / 1e3]
    q = Q("2C", "curve:pnl", lvl, "c_l2_pnl", seed,
          f"DV01-neutral 2s10s steepener, GBP 100m on the 10Y leg (Givens). 2Y moves {m2:+.0f}bp, 10Y {m10:+.0f}bp. What "
          f"kind of move is it, and what is your P&L?",
          [mcq("Curve move", LABELS, LABELS.index(lab)), num("P&L (GBP thousands)", "k", tol_rel=0.02, tol_abs=1)],
          "Explain.", "", [lab, "P&L = sum of -DV01 x move per leg"])
    attach_givens(q, g, labels, solver)
    exact = pnl(Composite([rec2, pay10]), c, move_curve(c, {2: m2, 10: m10}))
    q.model_answer = (f"**{lab}; P&L about {fmt_ccy(q.parts[1].correct * 1e3)}.**\n\n1. Each leg: -DV01 x its own move: "
                      f"2Y {fmt_ccy(-g['dv01_2y_leg'] * m2)}, 10Y {fmt_ccy(-g['dv01_10y_leg'] * m10)}.\n2. With matched DV01s "
                      f"that is DV01 x (change in 10Y - change in 2Y).\n3. Exact (engine, curve repriced): {fmt_ccy(exact)}.")
    return q


def c_l2_sizing(rng, lvl, seed):
    c = base_curve(); n10 = float(rng.choice([50e6, 100e6, 200e6]))
    d2 = risk(Swap(0, 2, par_swap_rate(c, 0, 2), 1e6, "receive"), c).dv01
    d10 = risk(Swap(0, 10, par_swap_rate(c, 0, 10), 1e6, "receive"), c).dv01
    g = {"n10_m": n10 / 1e6, "dv01_2y_per_1m": round(d2, 2), "dv01_10y_per_1m": round(d10, 2)}
    labels = {"n10_m": "10Y notional (GBP m)", "dv01_2y_per_1m": "2Y swap DV01 per GBP 1m (GBP/bp)",
              "dv01_10y_per_1m": "10Y swap DV01 per GBP 1m (GBP/bp)"}
    solver = lambda gv: [gv["n10_m"] * gv["dv01_10y_per_1m"] / gv["dv01_2y_per_1m"]]
    q = Q("2C", "curve:sizing", lvl, "c_l2_sizing", seed,
          f"You want a 2s10s steepener: pay fixed on GBP {n10/1e6:.0f}m 10Y. Using the DV01s in the Givens, how much 2Y "
          f"should you receive to be DV01-neutral?", [num("2Y notional (GBP m)", "m", tol_rel=0.02)],
          "Why match DV01 rather than notional?", "", ["Match DV01s", "Notional ratio = DV01_10 / DV01_2"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**About GBP {q.parts[0].correct:,.0f}m.**\n\n1. A curve trade should make money from the shape, not "
                      f"the level, so the two legs' DV01s must match.\n2. {n10/1e6:.0f}m x {g['dv01_10y_per_1m']} / "
                      f"{g['dv01_2y_per_1m']} = {q.parts[0].correct:,.0f}m.")
    return q


def c_l2_convexity_pnl(rng, lvl, seed):
    c = base_curve(); rec2, pay10 = _steepener(c); bp = int(rng.choice([75, 100, 150]))
    g = {"gamma_2y_leg": round(dv01_gamma(rec2, c), 2), "gamma_10y_leg": round(dv01_gamma(pay10, c), 2), "dy_bp": bp}
    labels = {"gamma_2y_leg": "Receive-2Y leg: change in DV01 per +1bp (GBP/bp per bp)",
              "gamma_10y_leg": "Pay-10Y leg: change in DV01 per +1bp (GBP/bp per bp)", "dy_bp": "Parallel move (bp, either way)"}
    solver = lambda gv: [-0.5 * (gv["gamma_2y_leg"] + gv["gamma_10y_leg"]) * gv["dy_bp"] ** 2 / 1e3]
    q = Q("2C", "curve:convexity", lvl, "c_l2_convexity_pnl", seed,
          f"Your DV01-neutral 2s10s steepener (GBP 100m 10Y leg) sees a {bp}bp parallel move with no change in slope. "
          f"Using the Givens, estimate the convexity P&L. Long or short convexity?",
          [num("Convexity P&L (GBP thousands)", "k", tol_rel=0.05, tol_abs=1), mcq("Convexity", LONG_SHORT, 1)],
          "Explain why a steepener is short convexity.", "",
          ["P&L ~ -0.5 (G2 + G10) dy^2", "Steepener short convexity", "10Y leg dominates"])
    attach_givens(q, g, labels, solver)
    book = Composite([rec2, pay10]); exact = pnl(book, c, c.shifted(bp))
    q.parts[1].correct = 0 if q.parts[0].correct > 0 else 1
    q.model_answer = (f"**About {fmt_ccy(q.parts[0].correct * 1e3)}: short convexity.**\n\n1. DV01-neutral, so the first-order "
                      f"terms cancel. What is left: -0.5 x (G_2Y + G_10Y) x dy^2.\n2. Paying 10Y makes the 10Y leg's DV01 "
                      f"move against you as rates move, and per unit of DV01 the 10Y has much more convexity than the 2Y.\n"
                      f"3. Exact (engine, +{bp}bp): {fmt_ccy(exact)}.")
    return q


def c_l3_full(rng, lvl, seed):
    c = base_curve(); n10 = float(rng.choice([50e6, 100e6, 200e6])); bp = float(rng.choice([25, 50]) * rng.choice([1, -1]))
    d2 = risk(Swap(0, 2, par_swap_rate(c, 0, 2), 1e6, "receive"), c).dv01
    d10 = risk(Swap(0, 10, par_swap_rate(c, 0, 10), 1e6, "receive"), c).dv01
    g = {"n10_m": n10 / 1e6, "dv01_2y_per_1m": round(d2, 2), "dv01_10y_per_1m": round(d10, 2), "dy_bp": bp}
    labels = {"n10_m": "10Y notional paid (GBP m)", "dv01_2y_per_1m": "2Y DV01 per GBP 1m (GBP/bp)",
              "dv01_10y_per_1m": "10Y DV01 per GBP 1m (GBP/bp)", "dy_bp": "Parallel move (bp)"}
    solver = lambda gv: [gv["n10_m"] * gv["dv01_10y_per_1m"] / gv["dv01_2y_per_1m"],
                         -(gv["n10_m"] * gv["dv01_2y_per_1m"] - gv["n10_m"] * gv["dv01_10y_per_1m"]) * gv["dy_bp"] / 1e3]
    q = Q("2C", "curve:sizing", lvl, "c_l3_full", seed,
          f"2s10s steepener paying fixed on GBP {n10/1e6:.0f}m 10Y. (a) How much 2Y do you receive to be DV01-neutral? "
          f"(b) If you used equal notionals instead, what would a {bp:+.0f}bp parallel move do to your P&L?",
          [num("(a) 2Y notional (GBP m)", "m", tol_rel=0.02), num("(b) Equal-notional P&L (GBP k)", "k", tol_rel=0.03, tol_abs=1)],
          "Explain what goes wrong with equal notionals.", "",
          ["Match DV01s", "Equal notionals leave net short duration", "Unintended directional bet"])
    attach_givens(q, g, labels, solver)
    eq = Composite([Swap(0, 2, par_swap_rate(c, 0, 2), n10, "receive"), Swap(0, 10, par_swap_rate(c, 0, 10), n10, "pay")])
    exact = pnl(eq, c, c.shifted(bp))
    q.model_answer = (f"**(a) GBP {q.parts[0].correct:,.0f}m; (b) about {fmt_ccy(q.parts[1].correct * 1e3)}.**\n\n1. Equal "
                      f"notionals leave you net short duration: net DV01 = {n10/1e6:.0f}m x ({g['dv01_2y_per_1m']} - "
                      f"{g['dv01_10y_per_1m']}) per bp.\n2. A parallel move then creates P&L that has nothing to do with "
                      f"the slope view.\n3. Exact (engine): {fmt_ccy(exact)}; the residual is convexity.")
    return q


def c_l3_fly(rng, lvl, seed):
    # PCA-weighted 2s5s10s fly: neutralise level and slope with loadings given
    lv = {"2": 1.0, "5": 1.05, "10": 0.95}
    sl = {"2": -0.6, "5": 0.05, "10": 0.55}
    lv = {k: round(v + float(rng.normal(0, 0.03)), 2) for k, v in lv.items()}
    sl = {k: round(v + float(rng.normal(0, 0.03)), 2) for k, v in sl.items()}
    g = {"belly_dv01": 100e3, "lev_2": lv["2"], "lev_5": lv["5"], "lev_10": lv["10"], "slope_2": sl["2"], "slope_5": sl["5"],
         "slope_10": sl["10"]}
    labels = {"belly_dv01": "Belly (5Y) DV01 you receive (GBP/bp)", "lev_2": "Level loading 2Y", "lev_5": "Level loading 5Y",
              "lev_10": "Level loading 10Y", "slope_2": "Slope loading 2Y", "slope_5": "Slope loading 5Y",
              "slope_10": "Slope loading 10Y"}

    def solver(gv):
        A = np.array([[gv["lev_2"], gv["lev_10"]], [gv["slope_2"], gv["slope_10"]]])
        b = np.array([gv["belly_dv01"] * gv["lev_5"], gv["belly_dv01"] * gv["slope_5"]])
        w2, w10 = np.linalg.solve(A, b)
        return [w2, w10]
    q = Q("2C", "curve:fly_pca", lvl, "c_l3_fly", seed,
          "You receive the 5Y in a 2s5s10s butterfly (belly DV01 in the Givens) and pay the wings. Choose wing DV01s so the "
          "trade is neutral to the first two PCA factors (level and slope), using the loadings given (bp move per unit "
          "factor move).", [num("2Y wing DV01 to pay (GBP/bp)", tol_rel=0.02), num("10Y wing DV01 to pay (GBP/bp)", tol_rel=0.02)],
          "Why PCA weights rather than 50/50 DV01 weights?", "",
          ["Solve two equations: level and slope exposures cancel", "50/50 DV01 leaves slope risk", "Residual = curvature view"])
    attach_givens(q, g, labels, solver)
    w2, w10 = q.parts[0].correct, q.parts[1].correct
    q.model_answer = (f"**Pay about {w2:,.0f} (2Y) and {w10:,.0f} (10Y) DV01.**\n\n1. Exposure to a factor = sum of DV01 x "
                      f"loading. Set level and slope exposure of the wings equal to the belly's:\n   w2 x L2 + w10 x L10 = "
                      f"B x L5 and w2 x S2 + w10 x S10 = B x S5.\n2. Solving gives the weights above (not 50/50).\n3. A "
                      f"50/50 DV01 fly is hedged for parallel moves only; when the curve steepens the wings move "
                      f"differently and you get slope P&L. PCA weights leave mostly curvature.")
    return q


# =============================================================================
# 2D Carry and roll-down
# =============================================================================
STEEP = {0.25: 2.75, 1: 3.0, 2: 3.3, 5: 3.9, 10: 4.4, 30: 4.8}


def d_l1(rng, lvl, seed):
    kind = str(rng.choice(["carry_sign", "kills"]))
    if kind == "carry_sign":
        return Q("2D", "carry:roll", lvl, "d_l1_sign", seed,
                 "The curve is steep and upward-sloping (3M SONIA 2.75%, 5Y 3.9%, 10Y 4.4%). You receive fixed in 5Y. Is your "
                 "carry positive or negative? Does roll-down help or hurt you?",
                 [mcq("Carry", ["Positive", "Negative"], 0), mcq("Roll-down", ["Helps", "Hurts"], 0)],
                 "Explain carry and roll-down.",
                 "**Positive carry, and roll-down helps.**\n\n1. Carry: you receive the 5Y fixed rate and pay the lower "
                 "short-term floating rate.\n2. Roll-down: on an unchanged curve your 5Y swap becomes a shorter swap, which is "
                 "priced at a lower rate, so receiving the original higher rate gains value.",
                 ["Receive fixed > pay floating", "Roll down a steep curve"])
    opts, corr = shuffle_opts(rng, "Rates rise by more than the carry plus roll over the horizon",
                              ["Rates stay exactly where they are", "The curve stays steep", "Rates fall"])
    return Q("2D", "carry:breakeven", lvl, "d_l1_kills", seed,
             "You receive 10Y on a steep curve for its carry and roll-down. What makes the trade lose money?",
             [mcq("Loses if", opts, corr)], "Explain the breakeven.",
             "**A rise in rates bigger than carry + roll.** Carry and roll are what you earn if nothing moves; they are your "
             "cushion. The breakeven is how many bp the rate can rise over the horizon before the duration loss eats it.",
             ["Breakeven = carry + roll in bp"])


def d_l2(rng, lvl, seed):
    c = ZeroCurve.from_pct(STEEP); T = int(rng.choice([5, 10])); h = 0.25
    g = {"par_T_pct": round(par_swap_rate(c, 0, T) * 100, 4), "par_T_minus_h_pct": round(par_swap_rate(c, 0, T - h) * 100, 4),
         "float_pct": round(c.fwd(0, 0.25) * 100, 4), "horizon_years": h}
    labels = {"par_T_pct": f"{T}Y par swap rate (%)", "par_T_minus_h_pct": f"{T - h:g}Y par swap rate (%)",
              "float_pct": "3M floating rate (%)", "horizon_years": "Horizon (years)"}
    solver = lambda gv: [(gv["par_T_pct"] - gv["float_pct"]) * 100 * gv["horizon_years"],
                         (gv["par_T_pct"] - gv["par_T_minus_h_pct"]) * 100]
    q = Q("2D", "carry:roll", lvl, "d_l2", seed,
          f"You receive fixed in {T}Y. Using the Givens, what are the 3-month carry and roll-down, in bp of rate?",
          [num("Carry (bp)", "bp", tol_abs=0.5, tol_rel=0.02), num("Roll-down (bp)", "bp", tol_abs=0.3, tol_rel=0.03)],
          "Explain each piece.", "", ["Carry = (fixed - floating) x horizon", "Roll = par(T) - par(T - h)"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**Carry {q.parts[0].correct:.1f}bp, roll {q.parts[1].correct:.1f}bp.**\n\n1. Carry = ({g['par_T_pct']} - "
                      f"{g['float_pct']})% x 0.25.\n2. Roll: in 3 months your swap is a {T - h:g}Y swap, priced at "
                      f"{g['par_T_minus_h_pct']}%; receiving {g['par_T_pct']}% vs that is the roll-down.")
    return q


def d_l3(rng, lvl, seed):
    c = ZeroCurve.from_pct(STEEP); h = 0.25
    g = {}
    for T in (5, 10):
        g[f"par_{T}"] = round(par_swap_rate(c, 0, T) * 100, 4)
        g[f"par_{T}_rolled"] = round(par_swap_rate(c, 0, T - h) * 100, 4)
    g["float_pct"] = round(c.fwd(0, 0.25) * 100, 4)
    g["dv01_10y"] = round(risk(Swap(0, 10, par_swap_rate(c, 0, 10), 100e6, "receive"), c).dv01, 0)
    labels = {"par_5": "5Y par (%)", "par_5_rolled": "4.75Y par (%)", "par_10": "10Y par (%)", "par_10_rolled": "9.75Y par (%)",
              "float_pct": "3M floating (%)", "dv01_10y": "DV01 of receiving GBP 100m 10Y (GBP/bp)"}

    def solver(gv):
        t5 = (gv["par_5"] - gv["float_pct"]) * 25 + (gv["par_5"] - gv["par_5_rolled"]) * 100
        t10 = (gv["par_10"] - gv["float_pct"]) * 25 + (gv["par_10"] - gv["par_10_rolled"]) * 100
        return [t5, t10, t10 * gv["dv01_10y"] / 1e3]
    q = Q("2D", "carry:breakeven", lvl, "d_l3", seed,
          "Using the Givens: (a) 3-month carry + roll (bp) for receiving 5Y, (b) the same for 10Y, (c) the GBP value of the "
          "10Y carry+roll on GBP 100m. Which tenor is better per unit of DV01, and what is the 10Y breakeven?",
          [num("(a) 5Y carry+roll (bp)", "bp", tol_abs=0.5), num("(b) 10Y carry+roll (bp)", "bp", tol_abs=0.5),
           num("(c) 10Y carry+roll (GBP k)", "k", tol_rel=0.03)],
          "Compare the two per DV01 and give the breakeven.", "",
          ["Carry + roll in bp is per unit DV01", "Breakeven = carry+roll in bp", "Compare tenors"])
    attach_givens(q, g, labels, solver)
    a, b, cc = (p.correct for p in q.parts)
    q.model_answer = (f"**5Y {a:.1f}bp, 10Y {b:.1f}bp; 10Y worth {fmt_ccy(cc * 1e3)}.**\n\n1. Carry + roll in bp of rate is "
                      f"already per unit of DV01, so compare them directly: {'5Y' if a > b else '10Y'} is better.\n2. The "
                      f"10Y breakeven is a {b:.1f}bp rise over 3 months before the trade loses.")
    return q


# =============================================================================
# 2E Pricing central banks
# =============================================================================
def e_l1(rng, lvl, seed):
    if rng.random() < 0.5:
        priced = -float(rng.choice([5, 8, 18, 20]))
        more = abs(priced) > 12.5
        return Q("2E", "cb:probabilities", lvl, "e_l1_read", seed,
                 f"SONIA prices **{priced:.0f}bp** for the next BoE meeting (moves come in 25bp). Does the market think a "
                 f"cut is more or less likely than not?",
                 [mcq("Market view", ["More likely than not", "Less likely than not"], 0 if more else 1)], "Explain.",
                 f"**{'More' if more else 'Less'} likely than not.** With only hold or a 25bp cut, priced change = p x (-25bp), "
                 f"so {abs(priced):.0f}bp means p {'above' if more else 'below'} 50% (12.5bp would be a coin toss).",
                 ["Priced bp / 25 = probability"])
    opts, corr = shuffle_opts(rng, "2Y yields rise: the market removes the cuts it had priced",
                              ["2Y yields fall", "Nothing: it was priced in", "Only 30Y yields move"])
    return Q("2E", "cb:reaction", lvl, "e_l1_react", seed,
             "SONIA prices -20bp for the next BoE meeting and the BoE holds. What happens to the front end?",
             [mcq("Reaction", opts, corr)], "Explain.",
             "**The front end sells off.** A hold surprises by about +20bp on that meeting and usually pushes out later cuts; "
             "2Y reprices most, typically a bear flattener.", ["Hawkish surprise vs pricing", "Front end sells off"])


def e_l2(rng, lvl, seed):
    priced = -float(rng.choice([5, 10, 15, 20, 30, 35]))
    g = {"priced_bp": priced, "step_bp": 25.0}
    labels = {"priced_bp": "Change priced for the meeting (bp)", "step_bp": "Size of one move (bp)"}
    solver = lambda gv: [((abs(gv["priced_bp"]) % gv["step_bp"]) / gv["step_bp"]) * 100]
    q = Q("2E", "cb:probabilities", lvl, "e_l2", seed,
          "SONIA pricing for the next BoE meeting is in the Givens. Assuming moves come in whole steps and any full step is "
          "certain, what probability is priced for the next (partial) step?",
          [num("Probability (%)", "%", tol_abs=1.5)], "Explain the calculation and its caveats.", "",
          ["p = priced / step (beyond full steps)", "Caveats: averaging, term premium"])
    attach_givens(q, g, labels, solver)
    full = int(abs(priced) // 25)
    q.model_answer = (f"**{q.parts[0].correct:.0f}%{f' on top of {full} certain 25bp cut' if full else ''}.**\n\n Expected "
                      f"change = full steps + p x 25bp. Caveats: meeting date vs averaging periods, term premium, and the chance "
                      f"of a 50bp move.")
    return q


def e_l3(rng, lvl, seed):
    p1 = -float(rng.choice([5, 10, 15, 20])); p2 = p1 - float(rng.choice([10, 15, 20, 25]))
    rate = CFG["boe_bank_rate"]
    g = {"bank_rate_pct": rate, "cum_m1_bp": p1, "cum_m2_bp": p2, "step_bp": 25.0}
    labels = {"bank_rate_pct": "Bank Rate now (%)", "cum_m1_bp": "Cumulative pricing by meeting 1 (bp)",
              "cum_m2_bp": "Cumulative pricing by meeting 2 (bp)", "step_bp": "Step size (bp)"}
    solver = lambda gv: [abs(gv["cum_m2_bp"] - gv["cum_m1_bp"]) / gv["step_bp"] * 100,
                         gv["bank_rate_pct"] + gv["cum_m2_bp"] / 100]
    q = Q("2E", "cb:path", lvl, "e_l3", seed,
          "Using the Givens: (a) what probability of a 25bp cut is priced AT meeting 2 (taking meeting 1's pricing as "
          "given)? (b) What expected Bank Rate is priced after meeting 2?",
          [num("(a) Probability at meeting 2 (%)", "%", tol_abs=1.5), num("(b) Expected rate after meeting 2 (%)", "%", tol_abs=0.01)],
          "Explain how you read a meeting path.", "", ["Incremental pricing between meetings", "Rate path = current + cumulative"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**(a) {q.parts[0].correct:.0f}%, (b) {q.parts[1].correct:.3f}%.**\n\n1. Meeting 2's own pricing = "
                      f"cumulative by 2 minus cumulative by 1 = {p2 - p1:.0f}bp, so p = {abs(p2 - p1):.0f}/25.\n2. Expected rate = "
                      f"{rate}% + ({p2:.0f}bp).")
    return q


# =============================================================================
# 2F Advanced
# =============================================================================
CONCEPTS = [
    ("advanced:swap_spreads", "Why can swap spreads (swap rate minus government yield) be negative, as in 30Y USD?",
     "Dealer balance-sheet costs make holding bonds expensive, heavy government supply cheapens bonds, and liability hedgers receive fixed, pushing swap rates below yields",
     ["Swaps carry more credit risk than government bonds", "The floating leg pays more than repo", "It is a free arbitrage that is always closed at once"],
     "Holding bonds uses scarce balance sheet; repo is not free; supply cheapens bonds; pensions receive long swaps. The 'arbitrage' needs balance sheet nobody has cheaply."),
    ("advanced:fly", "Why weight a 2s5s10s butterfly with PCA rather than 50/50 DV01?",
     "PCA weights hedge level and slope as they actually co-move, isolating curvature",
     ["DV01 weights are always wrong", "PCA weights are cheaper to execute", "PCA weights maximise carry"],
     "A 50/50 DV01 fly is only hedged to parallel moves; steepening moves the wings differently. PCA weights hedge both level and slope."),
    ("advanced:ldi_2022", "In September 2022, why did UK LDI funds sell gilts as yields spiked?",
     "Leveraged long-duration hedges lost value, collateral calls had to be met fast, so they sold gilts into a falling market until the BoE stepped in",
     ["They wanted to buy cheap gilts", "They were short duration and took profit", "Regulation forced a switch to equities"],
     "LDI funds hedge long liabilities with leveraged long duration. The mini-budget sent long yields up fast, the hedges needed collateral within days, and funds sold their most liquid asset: forced selling of duration, a doom loop."),
    ("advanced:delivery_option", "Why do bond futures usually trade cheap to the CTD's forward price?",
     "The short owns delivery options (which bond, when), and their value lowers the futures price",
     ["Futures have no carry", "Futures are more liquid so they trade rich", "The long chooses which bond to receive"],
     "The short's switch and timing options have value, so the long pays less: positive net basis equals the option value."),
    ("advanced:vol_owners", "Who is structurally SHORT rates volatility?",
     "MBS and callable-bond investors (short the prepayment/call option)",
     ["Mortgage servicers buying receivers", "Liability hedgers buying receiver swaptions", "Nobody: rates vol has no natural sellers"],
     "Holders of MBS and callables are short the borrower's or issuer's option, so they are short vol and short convexity; callable issuance and structured notes also supply vol."),
]


def f_l1(rng, lvl, seed):
    topic, q, ans, wrong, why = CONCEPTS[int(rng.integers(len(CONCEPTS)))]
    opts, corr = shuffle_opts(rng, ans, wrong)
    return Q("2F", topic, lvl, "f_l1_concept", seed, q, [mcq("Answer", opts, corr)], "Explain in your own words.",
             f"**{ans}.**\n\n{why}", [ans, why])


def f_l2_ctd(rng, lvl, seed):
    basket = [(0.04, 8.0), (0.05, 14.0), (0.035, 25.0)]
    y = float(rng.choice([0.03, 0.045, 0.075])); rows = ctd_analysis(basket, y)
    # futures trade below every bond's P/CF (positive basis everywhere: no arbitrage; the gap is carry + delivery option)
    F = round(min(r["p_over_cf"] for r in rows) - float(rng.uniform(0.1, 0.4)), 3)
    g = {"futures_price": F}
    labels = {"futures_price": "Futures price"}
    names = [f"{c*100:.1f}% {m:.0f}Y" for c, m in basket]
    for i, r in enumerate(rows):
        g[f"price_{i}"] = round(r["price"], 3); labels[f"price_{i}"] = f"{names[i]} price"
        g[f"cf_{i}"] = round(r["cf"], 4); labels[f"cf_{i}"] = f"{names[i]} conversion factor"
    solver = lambda gv: [min(gv[f"price_{i}"] - gv["futures_price"] * gv[f"cf_{i}"] for i in range(3))]
    basis = [g[f"price_{i}"] - F * g[f"cf_{i}"] for i in range(3)]
    ctd = int(np.argmin(basis))
    q = Q("2F", "advanced:ctd", lvl, "f_l2_ctd", seed,
          "Using the prices, conversion factors and futures price in the Givens, which bond is cheapest to deliver, and what "
          "is its gross basis?", [mcq("CTD", names, ctd), num("CTD gross basis (price points)", tol_abs=0.01)],
          "Explain how the short chooses.", "", ["Gross basis = price - futures x CF", "CTD = lowest basis"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**{names[ctd]}, basis {q.parts[1].correct:.3f}.**\n\n1. The short delivers the bond that costs least "
                      f"relative to what they are paid (futures x CF): lowest gross basis.\n2. Bases: " +
                      ", ".join(f"{n} {b:.3f}" for n, b in zip(names, basis)) +
                      f".\n3. At yields {'above' if y > 0.06 else 'below'} the 6% notional coupon, "
                      f"{'high' if y > 0.06 else 'low'}-duration bonds tend to be CTD.")
    return q


def f_l2_normal_vol(rng, lvl, seed):
    F = float(rng.choice([3.0, 3.5, 4.0, 4.5])); sb = float(rng.choice([20, 22, 25, 30]))
    g = {"forward_pct": F, "black_vol_pct": sb}
    labels = {"forward_pct": "Forward swap rate (%)", "black_vol_pct": "Lognormal (Black) vol (%)"}
    solver = lambda gv: [gv["black_vol_pct"] / 100 * gv["forward_pct"] / 100 * 1e4, gv["black_vol_pct"] / 100 * gv["forward_pct"] / 100 * 1e4 / np.sqrt(252)]
    q = Q("2F", "advanced:normal_vol", lvl, "f_l2_nvol", seed,
          "Convert the lognormal vol in the Givens to an approximate normal (bp) vol, and to a daily bp move.",
          [num("Normal vol (bp/yr)", "bp", tol_rel=0.02), num("Daily move (bp, 252 days)", "bp", tol_rel=0.03)],
          "Why do rates desks quote normal vol?", "", ["sigma_N ~ sigma_B x F", "Daily = annual / sqrt(252)"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**About {q.parts[0].correct:.0f}bp a year, {q.parts[1].correct:.1f}bp a day.** Near the money "
                      f"sigma_N ~ sigma_B x F. Rate moves are closer to additive than proportional (and rates can go "
                      f"negative), so desks quote normal vol.")
    return q


def f_l3_krd(rng, lvl, seed):
    c = base_curve(); m = int(rng.choice([7, 12, 20])); b = Bond(0.045, m, 100e6); pillars = [2, 5, 10, 20, 30]
    kr = key_rate_dv01s(b.pv, c, pillars)
    hedge_dv01 = {p: risk(Swap(0, p, par_swap_rate(c, 0, p), 1e6, "pay"), c).dv01 for p in pillars}
    g = {}
    labels = {}
    for p in pillars:
        g[f"kr_{p}"] = round(kr[p], 0); labels[f"kr_{p}"] = f"Bond key-rate DV01 at {p}Y (GBP/bp)"
    for p in (5, 10, 20):
        g[f"pay_dv01_{p}"] = round(hedge_dv01[p], 2); labels[f"pay_dv01_{p}"] = f"DV01 of paying GBP 1m {p}Y swap (GBP/bp)"
    big = sorted(pillars, key=lambda p: -abs(kr[p]))[:2]
    solver = lambda gv: [-gv[f"kr_{p}"] / gv[f"pay_dv01_{p}"] for p in (5, 10, 20)]
    q = Q("2F", "advanced:krd", lvl, "f_l3_krd", seed,
          f"You own GBP 100m of a 4.5% {m}Y gilt. Hedge its 5Y, 10Y and 20Y key-rate DV01s by paying fixed in 5Y, 10Y and "
          f"20Y swaps (assume each swap's DV01 sits in its own bucket). How much notional of each (GBP m)?",
          [num("5Y swap (GBP m)", "m", tol_rel=0.02, tol_abs=0.2), num("10Y swap (GBP m)", "m", tol_rel=0.02, tol_abs=0.2),
           num("20Y swap (GBP m)", "m", tol_rel=0.02, tol_abs=0.2)], "What does key-rate DV01 tell you that parallel DV01 does not?",
          "", ["Notional = -KR DV01 / swap DV01 per 1m", "Hedge per bucket", "Residual curve risk"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**5Y {q.parts[0].correct:.1f}m, 10Y {q.parts[1].correct:.1f}m, 20Y {q.parts[2].correct:.1f}m.**\n\n1. "
                      f"Key-rate DV01 bumps one pillar at a time, showing WHERE the duration sits (here mostly "
                      f"{big[0]}Y and {big[1]}Y).\n2. Each hedge = bucket DV01 / DV01 of paying GBP 1m in that tenor.\n3. "
                      f"Simplification: real swaps spread DV01 across neighbouring buckets, so you would solve the full matrix.")
    q.charts = [chart_bar("Bond key-rate DV01 (GBP/bp)", [f"{p}Y" for p in pillars], [kr[p] for p in pillars], "GBP")]
    return q


def f_l3_ldi(rng, lvl, seed):
    dv = float(rng.choice([2e6, 3e6, 5e6])); move = float(rng.choice([100, 120, 150])); coll = float(rng.choice([300e6, 400e6, 600e6]))
    g = {"hedge_dv01": dv, "yield_move_bp": move, "collateral_pool": coll}
    labels = {"hedge_dv01": "DV01 of the fund's receive-fixed / repo gilt hedges (GBP/bp)", "yield_move_bp": "Rise in long gilt yields (bp)",
              "collateral_pool": "Liquid collateral available (GBP)"}
    solver = lambda gv: [gv["hedge_dv01"] * gv["yield_move_bp"] / 1e6, gv["collateral_pool"] / gv["hedge_dv01"]]
    q = Q("2F", "advanced:ldi_2022", lvl, "f_l3_ldi", seed,
          "An LDI fund hedges pension liabilities with leveraged long duration (Givens). Long gilt yields jump. (a) How much "
          "collateral is called (GBP m)? (b) How many bp can yields rise before the liquid collateral runs out?",
          [num("(a) Collateral call (GBP m)", "m", tol_rel=0.01), num("(b) bp until collateral is exhausted", "bp", tol_rel=0.01)],
          "Explain the 2022 doom loop.", "", ["Collateral call ~ DV01 x move", "Forced selling of gilts raises yields further"])
    attach_givens(q, g, labels, solver)
    q.model_answer = (f"**(a) GBP {q.parts[0].correct:,.0f}m, (b) {q.parts[1].correct:.0f}bp.**\n\n1. The hedges lose ~DV01 x "
                      f"move, paid as variation margin. Liabilities fall in value too, but they need no cash.\n2. Once "
                      f"liquid collateral runs out, funds sell gilts, which pushes yields up, which triggers more calls: a "
                      f"doom loop that the BoE broke by buying long gilts.")
    return q


TOPICS = {
    "2B": ("Convexity intuition", {1: [b_l1_barbell, b_l1_mortgage, b_l1_cost], 2: [b_l2_maturity, b_l2_barbell],
                                   3: [b_l3_straddle]}),
    "2C": ("Curve trades", {1: [c_l1_label, c_l1_convexity, c_l1_convexity, c_l1_boe], 2: [c_l2_pnl, c_l2_sizing, c_l2_convexity_pnl],
                            3: [c_l3_full, c_l3_fly]}),
    "2D": ("Carry and roll-down", {1: [d_l1], 2: [d_l2], 3: [d_l3]}),
    "2E": ("Pricing central banks", {1: [e_l1], 2: [e_l2], 3: [e_l3]}),
    "2F": ("Advanced", {1: [f_l1], 2: [f_l2_ctd, f_l2_normal_vol], 3: [f_l3_krd, f_l3_ldi]}),
}


def make_generator(code: str):
    levels = TOPICS[code][1]

    def gen(seed: int, difficulty: int):
        rng = np.random.default_rng(seed)
        fns = levels[difficulty]
        return fns[int(rng.integers(len(fns)))](rng, difficulty, seed)
    return gen

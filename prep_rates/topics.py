"""Sections 2B-2F: convexity, curve trades, carry/roll, central-bank pricing, advanced."""
from __future__ import annotations

import numpy as np

from engine.config import load_config
from engine.rates import (BP, ZeroCurve, bond_risk, ctd_analysis, implied_move_probability, key_rate_dv01s,
                          par_swap_rate, receiver_carry_rolldown)
from grading.question import Part, Question, chart_bar, chart_line
from prep_rates.instruments import (Bond, Composite, Swap, Swaption, base_curve, callable_bond, fmt_ccy,
                                    move_curve, pnl, risk)

CFG = load_config()["rates_engine"]
NVOL = CFG["swaption_normal_vol_bp"] / 1e4


# ---------------------------------------------------------------------------
# 2B Convexity
# ---------------------------------------------------------------------------
def b_barbell(rng, d, seed):
    c = base_curve()
    s, l, m = 2, 30, 10
    bullet = Bond(0.0, m, 100e6)
    rb = risk(bullet, c)
    short, long_ = Bond(0.0, s, 1.0), Bond(0.0, l, 1.0)
    # solve weights: same PV and same DV01 as the bullet
    A = np.array([[short.pv(c), long_.pv(c)], [risk(short, c).dv01, risk(long_, c).dv01]])
    w = np.linalg.solve(A, np.array([rb.pv, rb.dv01]))
    barbell = Composite([Bond(0.0, s, w[0]), Bond(0.0, l, w[1])])
    bp = int(rng.choice([75, 100, 150]))
    diff_dn = pnl(barbell, c, c.shifted(-bp)) - pnl(bullet, c, c.shifted(-bp))
    diff_up = pnl(barbell, c, c.shifted(bp)) - pnl(bullet, c, c.shifted(bp))
    y_bullet = float(c.zero(m))
    y_bar = float((w[0] * short.pv(c) * c.zero(s) * s + w[1] * long_.pv(c) * c.zero(l) * l) /
                  (w[0] * short.pv(c) * s + w[1] * long_.pv(c) * l))
    moves = np.arange(-150, 151, 25)
    model = (f"**The barbell outperforms in both directions: {fmt_ccy(diff_dn)} if yields fall {bp}bp, "
             f"{fmt_ccy(diff_up)} if they rise {bp}bp.**\n\n"
             f"1. Same PV and duration, but the barbell spreads its cash flows out (2y and 30y), and convexity grows "
             f"roughly with maturity squared, so the 30y wing adds far more convexity than the 2y wing gives up.\n"
             f"2. Convexity P&L (+/-25bp): barbell {fmt_ccy(risk(barbell, c).convexity_pnl)} vs bullet "
             f"{fmt_ccy(rb.convexity_pnl)}.\n"
             f"3. You pay for it: in a fair market the extra convexity costs yield. Here the duration-weighted yield of "
             f"the barbell is {y_bar*100:.2f}% vs {y_bullet*100:.2f}% for the bullet. The barbell is also SHORT the "
             f"belly versus the wings: if the 10y richens relative to 2y/30y (non-parallel move) it loses.\n"
             f"4. Same trade-off as gamma vs theta in options.")
    return Question("rates", "2B", "convexity:barbell", d, "b_barbell", seed,
                    prompt=(f"Compare GBP 100m PV of a 10y zero (bullet) with a 2y/30y zero barbell of the **same PV and DV01**. "
                            f"Yields move {bp}bp in parallel, up or down. Which does better, and by how much if yields fall?"),
                    parts=[Part("mcq", "Better in a big move", ["Barbell, in either direction", "Bullet, in either direction",
                                                                "Barbell if yields fall, bullet if they rise"], 0),
                           Part("numeric", f"Barbell minus bullet P&L if yields fall {bp}bp (GBP k)",
                                correct=diff_dn / 1e3, tol_abs=max(5.0, 0.15 * abs(diff_dn / 1e3)))],
                    free_text_prompt="What do you give up for that convexity?",
                    facts={"weights_2y_30y_face": list(map(float, w)), "diff_down": diff_dn, "diff_up": diff_up,
                           "yield_barbell": y_bar, "yield_bullet": y_bullet}, model_answer=model,
                    rubric=["Barbell has more convexity", "Gains in big moves both ways", "Costs yield / carry",
                            "Exposed to belly vs wings (curve shape)"],
                    charts=[chart_line("Barbell minus bullet P&L", moves,
                                       {"Barbell - bullet": [pnl(barbell, c, c.shifted(x)) - pnl(bullet, c, c.shifted(x)) for x in moves]},
                                       "Parallel move (bp)", "GBP", vline=0)])


def b_maturity_squared(rng, d, seed):
    y = 0.04
    t1, t2 = rng.choice([(5, 10), (5, 20), (10, 30), (2, 10)])
    t1, t2 = int(t1), int(t2)
    c1, c2 = bond_risk(y, 0.0, t1, 1).convexity, bond_risk(y, 0.0, t2, 1).convexity
    ratio = c2 / c1
    model = (f"**About {ratio:.1f}x.**\n\n1. Convexity measures how much duration changes as yields move. For a zero, "
             f"convexity = T(T+1)/(1+y)^2, roughly maturity squared.\n2. Engine: {t1}y zero {c1:.1f}, {t2}y zero "
             f"{c2:.1f}; ratio {ratio:.2f} (maturity-squared rule gives {(t2/t1)**2:.1f}).\n3. Desk takeaway: "
             f"convexity lives at the long end; 30y paper is where long-convexity demand (and mortgage hedging "
             f"flows) bites hardest.")
    return Question("rates", "2B", "convexity:maturity", d, "b_mat2", seed,
                    prompt=f"Roughly how many times more convexity does a {t2}y zero-coupon bond have than a {t1}y zero (yield 4%)?",
                    parts=[Part("numeric", "Ratio", correct=ratio, tol_rel=0.15, unit="x")],
                    free_text_prompt="Explain the scaling.", facts={"c1": c1, "c2": c2, "ratio": ratio},
                    model_answer=model, rubric=["Convexity ~ T^2", f"Ratio about {ratio:.1f}"])


def b_long_convexity_cost(rng, d, seed):
    c = base_curve()
    F = par_swap_rate(c, 1, 11)
    straddle = Composite([Swaption(1, 10, F, NVOL, "payer", 100e6), Swaption(1, 10, F, NVOL, "receiver", 100e6)])
    prem = straddle.pv(c)
    from engine.rates import annuity
    A_fwd = annuity(c, 1, 11) * 100e6
    be = prem / A_fwd / BP
    model = (f"**You need the 10y swap rate (1y forward) to move about {be:.0f}bp either way by expiry.**\n\n"
             f"1. A swaption straddle is pure long convexity: it gains from big moves in either direction.\n"
             f"2. You pay for it up front: premium {fmt_ccy(prem)}. At expiry the payoff is about "
             f"annuity x |move|, with annuity PV ~ {fmt_ccy(A_fwd*BP)} per bp.\n3. Breakeven = premium / (annuity per bp) "
             f"= {be:.0f}bp. With {NVOL*1e4:.0f}bp normal vol, the expected absolute move over 1y is about "
             f"{NVOL*1e4*0.798:.0f}bp (0.8 x sigma).\n4. Same as options: long gamma costs theta; long convexity "
             f"costs carry or yield.")
    return Question("rates", "2B", "convexity:cost", d, "b_cost", seed,
                    prompt=(f"You buy GBP 100m of a 1y-into-10y ATM swaption straddle (payer + receiver) at {NVOL*1e4:.0f}bp "
                            f"normal vol. Roughly how far must rates move by expiry (bp, either way) to break even?"),
                    parts=[Part("numeric", "Breakeven move (bp)", correct=be, tol_rel=0.1, unit="bp")],
                    free_text_prompt="How is this like gamma vs theta?",
                    facts={"premium": prem, "annuity_per_bp": A_fwd * BP, "breakeven_bp": be, "normal_vol_bp": NVOL * 1e4},
                    model_answer=model, rubric=["Long convexity costs premium", "Breakeven = premium / annuity", "Gamma-theta analogy"])


def b_mortgage(rng, d, seed):
    c = base_curve()
    cb = callable_bond(0.045, 10, 2, 100e6, NVOL, c)
    r0, r1 = risk(cb, c), risk(cb, c.shifted(-50))
    opts = ["Receive fixed / buy duration, which pushes yields lower still",
            "Pay fixed / sell duration, which pushes yields back up",
            "Nothing: MBS duration does not depend on rates"]
    model = (f"**{opts[0]}.**\n\n1. Mortgage holders are short the borrower's prepayment option: when rates fall, "
             f"borrowers refinance, the bond pays back early and its duration SHORTENS (negative convexity).\n"
             f"2. Engine (callable bond proxy): DV01 {fmt_ccy(r0.dv01)} now, {fmt_ccy(r1.dv01)} after rates fall 50bp.\n"
             f"3. Investors who target a duration must buy duration back (receive fixed, buy long bonds) as rates fall, "
             f"and sell as rates rise. That flow chases the market and amplifies moves: 'convexity hedging'.")
    return Question("rates", "2B", "convexity:mortgage", d, "b_mbs", seed,
                    prompt="Rates rally hard. What do MBS holders who hedge their duration do, and what does that do to the market?",
                    parts=[Part("mcq", "Hedging flow", opts, 0)], free_text_prompt="Explain the chain.",
                    facts={"dv01_now": r0.dv01, "dv01_after_rally": r1.dv01}, model_answer=model,
                    rubric=["Prepayment shortens duration as rates fall", "Hedgers buy duration", "Amplifies the move"])


# ---------------------------------------------------------------------------
# 2C Curve trades
# ---------------------------------------------------------------------------
LABELS = ["Bull steepener", "Bull flattener", "Bear steepener", "Bear flattener"]
DRIVERS = {
    "Bull steepener": "front end falls more: markets price earlier or deeper central-bank cuts",
    "Bull flattener": "long end falls more: growth or inflation fears, flight to duration, long-end demand",
    "Bear steepener": "long end rises more: term premium, supply, fiscal worries, inflation risk",
    "Bear flattener": "front end rises more: central bank hiking or pricing out cuts",
}


def _dv01_neutral_steepener(c, n10=100e6):
    p2, p10 = par_swap_rate(c, 0, 2), par_swap_rate(c, 0, 10)
    pay10 = Swap(0, 10, p10, n10, "pay")
    d10 = abs(risk(pay10, c).dv01)
    d2u = risk(Swap(0, 2, p2, 1.0, "receive"), c).dv01
    rec2 = Swap(0, 2, p2, d10 / d2u, "receive")
    return rec2, pay10


def c_label(rng, d, seed):
    c = base_curve()
    lab = str(rng.choice(LABELS))
    a, b = sorted([float(rng.integers(5, 15)), float(rng.integers(20, 40))])
    bull = lab.startswith("Bull")
    steep = lab.endswith("steepener")
    if bull:
        m2, m10 = (-b, -a) if steep else (-a, -b)
    else:
        m2, m10 = (a, b) if steep else (b, a)
    rec2, pay10 = _dv01_neutral_steepener(c)
    book = Composite([rec2, pay10])
    moved = move_curve(c, {2: m2, 10: m10})
    p = pnl(book, c, moved)
    model = (f"**{lab}; your DV01-neutral 2s10s steepener makes {fmt_ccy(p)}.**\n\n"
             f"1. Bull = yields fall, bear = yields rise. Steepener = 10y minus 2y widens; flattener = it narrows.\n"
             f"2. 2y {m2:+.0f}bp, 10y {m10:+.0f}bp: the curve {'steepened' if m10 - m2 > 0 else 'flattened'} by "
             f"{abs(m10 - m2):.0f}bp. Typical driver: {DRIVERS[lab]}.\n"
             f"3. Steepener = receive 2y, pay 10y, DV01-matched: P&L ~ DV01 x (change in 10y - change in 2y) = "
             f"{fmt_ccy(risk(pay10, c).dv01 * -1)} per bp x {m10 - m2:+.0f} ~ {fmt_ccy(p)}.")
    return Question("rates", "2C", "curve:labels", d, "c_label", seed,
                    prompt=(f"2y SONIA swaps move **{m2:+.0f}bp** and 10y move **{m10:+.0f}bp**. What kind of move is "
                            f"this? What is the P&L of a DV01-neutral 2s10s steepener with GBP 100m on the 10y leg?"),
                    parts=[Part("mcq", "Curve move", LABELS, LABELS.index(lab)),
                           Part("numeric", "Steepener P&L (GBP k)", correct=p / 1e3, tol_abs=max(3.0, 0.1 * abs(p / 1e3)))],
                    free_text_prompt="What typically drives this kind of move?",
                    facts={"move_2y": m2, "move_10y": m10, "label": lab, "steepener_pnl": p,
                           "dv01_10y_leg": risk(pay10, c).dv01, "dv01_2y_leg": risk(rec2, c).dv01},
                    model_answer=model, rubric=[lab, "Steepener P&L ~ DV01 x (d10 - d2)", DRIVERS[lab]])


def c_sizing(rng, d, seed):
    c = base_curve()
    n10 = float(rng.choice([50e6, 100e6, 200e6]))
    rec2, pay10 = _dv01_neutral_steepener(c, n10)
    ratio = rec2.notional / n10
    eq = Composite([Swap(0, 2, rec2.fixed, n10, "receive"), pay10])
    bp = float(rng.choice([25, 50]) * rng.choice([1, -1]))
    p_eq = pnl(eq, c, c.shifted(bp))
    p_w = pnl(Composite([rec2, pay10]), c, c.shifted(bp))
    model = (f"**Receive about GBP {rec2.notional/1e6:,.0f}m of 2y ({ratio:.2f}x the 10y notional).**\n\n"
             f"1. A curve trade should make money from the SHAPE changing, not the LEVEL. So match DV01s, not notionals.\n"
             f"2. 10y DV01 {fmt_ccy(-risk(pay10, c).dv01)} per bp vs 2y DV01 per GBP 1m "
             f"{fmt_ccy(risk(Swap(0, 2, rec2.fixed, 1e6, 'receive'), c).dv01)}: ratio {ratio:.2f}.\n"
             f"3. Equal notionals leave you net short duration (the 10y leg dominates): a {bp:+.0f}bp parallel move gives "
             f"{fmt_ccy(p_eq)} instead of {fmt_ccy(p_w)} for the DV01-neutral version. That is an unintended "
             f"directional bet.")
    return Question("rates", "2C", "curve:sizing", d, "c_sizing", seed,
                    prompt=(f"You want a 2s10s steepener: pay fixed on GBP {n10/1e6:.0f}m 10y. How much 2y should you "
                            f"receive to be DV01-neutral? What goes wrong with equal notionals if rates move {bp:+.0f}bp in parallel?"),
                    parts=[Part("numeric", "2y notional (GBP m)", correct=rec2.notional / 1e6, tol_rel=0.08, unit="m"),
                           Part("numeric", f"Equal-notional P&L for {bp:+.0f}bp parallel (GBP k)", correct=p_eq / 1e3,
                                tol_abs=max(3.0, 0.1 * abs(p_eq / 1e3)))],
                    free_text_prompt="Explain DV01 weighting.",
                    facts={"notional_2y": rec2.notional, "ratio": ratio, "pnl_equal_notional": p_eq, "pnl_dv01_neutral": p_w},
                    model_answer=model, rubric=["Match DV01 not notional", f"Ratio ~{ratio:.1f}x", "Equal notional = residual duration"])


def c_boe_view(rng, d, seed):
    c = base_curve()
    opts = ["Receive 2y SONIA vs pay 10y, DV01-weighted (2s10s steepener)",
            "Pay 2y vs receive 10y (flattener)", "Pay 10y outright", "Buy 30y gilts outright"]
    rec2, pay10 = _dv01_neutral_steepener(c)
    model = (f"**{opts[0]}.**\n\n1. Earlier cuts pull down expected policy rates over the next 1-2 years, so the front "
             f"end rallies most: a bull steepener. Receiving the 2y captures it; paying 10y DV01-neutral removes the "
             f"bet on the overall level.\n2. Sizing: pay GBP 100m 10y, receive ~GBP {rec2.notional/1e6:,.0f}m 2y "
             f"(DV01 {fmt_ccy(risk(rec2, c).dv01)} vs {fmt_ccy(risk(pay10, c).dv01)} per bp).\n3. Purer alternatives: "
             f"receive a specific meeting-dated OIS or SONIA futures around the meeting you think is mispriced.\n"
             f"4. Risks: the cuts come with growth fears that rally the long end too (bull flattener), or term "
             f"premium falls.")
    return Question("rates", "2C", "curve:expression", d, "c_boe", seed,
                    prompt="You think the BoE cuts sooner than the market prices. What curve trade do you put on, and how do you size it?",
                    parts=[Part("mcq", "Trade", opts, 0)], free_text_prompt="Explain the trade, sizing and risks.",
                    facts={"notional_2y_for_100m_10y": rec2.notional}, model_answer=model,
                    rubric=["Receive front end / steepener", "DV01-neutral sizing", "Risks"])


# ---------------------------------------------------------------------------
# 2D Carry and roll-down
# ---------------------------------------------------------------------------
def d_carry_roll(rng, d, seed):
    c = ZeroCurve.from_pct({0.25: 2.75, 1: 3.0, 2: 3.3, 5: 3.9, 10: 4.4, 30: 4.8})
    h = 0.25
    r5, r10 = receiver_carry_rolldown(c, 5, h), receiver_carry_rolldown(c, 10, h)
    better = 0 if r5["total_bp"] > r10["total_bp"] else 1
    ask = int(rng.choice([5, 10]))
    rr = r5 if ask == 5 else r10
    model = (f"**Receiving {ask}y: carry {rr['carry_bp']:.1f}bp + roll {rr['roll_bp']:.1f}bp = {rr['total_bp']:.1f}bp "
             f"over 3 months.**\n\n1. Carry: you receive the fixed rate and pay the (lower) short floating rate: "
             f"({rr['par_rate']*100:.2f}% - {rr['float_rate']*100:.2f}%) x 0.25.\n2. Roll-down: on an unchanged, "
             f"upward-sloping curve your {ask}y swap becomes a {ask - h:.2f}y swap, which is priced at a lower rate, "
             f"so it gains in value.\n3. 5y: {r5['total_bp']:.1f}bp vs 10y: {r10['total_bp']:.1f}bp (per unit DV01). "
             f"The {['5y', '10y'][better]} wins here; note how the carry/roll split differs between the two, and that "
             f"carry is earned only if the curve does not move.\n4. Breakeven: rates can "
             f"rise ~{rr['total_bp']:.0f}bp in {ask}y over the 3 months before the trade loses.")
    return Question("rates", "2D", "carry:roll", d, "d_carry", seed,
                    prompt=(f"Curve (zero rates): 3M 2.75%, 1y 3.0%, 2y 3.3%, 5y 3.9%, 10y 4.4%, 30y 4.8%. What is the "
                            f"3-month carry plus roll-down (bp of rate) on receiving the **{ask}y** swap? Which is better per "
                            f"DV01: receiving 5y or 10y?"),
                    parts=[Part("numeric", f"{ask}y carry + roll (bp)", correct=rr["total_bp"], tol_abs=max(1.0, 0.1 * abs(rr["total_bp"]))),
                           Part("mcq", "Better per DV01", ["5y", "10y"], better)],
                    free_text_prompt="Explain carry, roll-down and the breakeven.",
                    facts={"5y": r5, "10y": r10, "horizon_years": h}, model_answer=model,
                    rubric=["Carry = fixed - floating", "Roll-down from curve slope", "Breakeven in bp"],
                    charts=[chart_bar("Carry + roll over 3M (bp)", ["5y carry", "5y roll", "10y carry", "10y roll"],
                                      [r5["carry_bp"], r5["roll_bp"], r10["carry_bp"], r10["roll_bp"]], "bp")])


# ---------------------------------------------------------------------------
# 2E Central-bank pricing
# ---------------------------------------------------------------------------
def e_probability(rng, d, seed):
    cb = str(rng.choice(["BoE (SONIA)", "Fed (SOFR / fed funds)"]))
    if d == 1:
        priced = -float(rng.choice([5, 10, 15, 20]))
        r = implied_move_probability(priced)
        ans = r["prob_next_step"] * 100
        prompt = f"{cb} OIS prices **{priced:.0f}bp** for the next meeting. Assuming the choice is hold or a 25bp cut, what is the implied probability of a cut?"
        steps = f"probability = {abs(priced):.0f} / 25 = {ans:.0f}%."
    else:
        p1 = -float(rng.choice([5, 10, 15, 20]))
        p2 = p1 - float(rng.choice([10, 15, 20, 25]))
        incr = p2 - p1
        ans = abs(incr) / 25 * 100
        r = {"meeting1": p1, "cumulative_meeting2": p2}
        prompt = (f"{cb} OIS prices **{p1:.0f}bp** cumulative by meeting 1 and **{p2:.0f}bp** cumulative by meeting 2. "
                  f"Holding the meeting-1 pricing as given, what probability of a 25bp cut is priced AT meeting 2?")
        steps = f"incremental pricing at meeting 2 = {p2:.0f} - ({p1:.0f}) = {incr:.0f}bp, so probability = {abs(incr):.0f}/25 = {ans:.0f}%."
    model = (f"**{ans:.0f}%.**\n\n1. OIS forwards price the expected policy rate. With only 'hold' or 'cut 25bp' "
             f"possible, the expected change = p x (-25bp).\n2. So {steps}\n3. Caveats: meeting dates vs averaging "
             f"periods, term premium, and the chance of a 50bp move all blur this.")
    return Question("rates", "2E", "cb:probabilities", d, "e_prob", seed, prompt=prompt,
                    parts=[Part("numeric", "Probability (%)", correct=ans, tol_abs=2.0, unit="%")],
                    free_text_prompt="Explain the calculation and its caveats.", facts=dict(r, answer_pct=ans),
                    model_answer=model, rubric=["Expected change = p x step", f"{ans:.0f}%"])


def e_reaction(rng, d, seed):
    priced = -float(rng.choice([15, 20]))
    p = abs(priced) / 25
    opts = ["2y yields rise: the market removes the cuts it had priced", "2y yields fall",
            "Nothing: it was priced in", "Only 30y yields move"]
    model = (f"**{opts[0]}.**\n\n1. {abs(priced):.0f}bp priced = a {p*100:.0f}% cut probability. A hold surprises "
             f"the market by about +{abs(priced):.0f}bp on that meeting, and usually pushes out the expected path of "
             f"later cuts too.\n2. The front end (2y) reprices most: a bear flattener is typical.\n3. A receiver of 2y "
             f"loses ~DV01 x the move.")
    return Question("rates", "2E", "cb:reaction", d, "e_react", seed,
                    prompt=f"SONIA prices {priced:.0f}bp for the next BoE meeting and the BoE holds. What happens to the front end?",
                    parts=[Part("mcq", "Reaction", opts, 0)], free_text_prompt="Explain.",
                    facts={"priced_bp": priced, "implied_prob": p}, model_answer=model,
                    rubric=["Hold = hawkish surprise vs pricing", "Front end sells off", "Bear flattener"])


# ---------------------------------------------------------------------------
# 2F Advanced
# ---------------------------------------------------------------------------
def f_ctd(rng, d, seed):
    basket = [(0.04, 8.0), (0.05, 14.0), (0.035, 25.0)]
    y = float(rng.choice([0.03, 0.045, 0.075]))
    rows = ctd_analysis(basket, y)
    ctd = [i for i, r in enumerate(rows) if r["ctd"]][0]
    names = [f"{c*100:.1f}% {m:.0f}y" for c, m in basket]
    model = (f"**CTD: {names[ctd]}.**\n\n1. The short chooses which bond to deliver and picks the one cheapest relative "
             f"to its invoice price (futures x CF). Conversion factors price every bond at the notional coupon "
             f"(6% here), which is only fair when yields are at 6%.\n2. When yields are above the notional coupon, "
             f"high-duration bonds have fallen furthest in price relative to their CF, so they become CTD. When yields "
             f"are below it, low-duration bonds are CTD.\n3. Engine at {y*100:.1f}%: " +
             "; ".join(f"{names[i]} P/CF {r['p_over_cf']:.2f}, basis {r['gross_basis']:.2f}" for i, r in enumerate(rows)) +
             ".\n4. The short's switch option (and timing / end-of-month options) makes futures trade cheap to the "
             "CTD's forward: the delivery option.")
    return Question("rates", "2F", "advanced:ctd", d, "f_ctd", seed,
                    prompt=f"A futures basket has {', '.join(names)}. Notional coupon 6%, all bonds yield {y*100:.1f}%. Which bond is cheapest to deliver?",
                    parts=[Part("mcq", "CTD", names, ctd)], free_text_prompt="Why, and what is the short's delivery option?",
                    facts={"rows": rows, "yield": y}, model_answer=model,
                    rubric=["CTD minimises price - F x CF", "Yields above notional coupon favour high duration",
                            "Delivery option belongs to the short"])


def f_normal_vol(rng, d, seed):
    F = float(rng.choice([0.03, 0.035, 0.04, 0.045]))
    sb = float(rng.choice([0.2, 0.22, 0.25, 0.3]))
    sn = sb * F * 1e4
    model = (f"**About {sn:.0f}bp.**\n\n1. Rates vol is quoted in normal (bp) terms because rate moves are closer to "
             f"additive than proportional, and rates can go negative.\n2. Near the money, sigma_normal ~ "
             f"sigma_lognormal x F = {sb*100:.0f}% x {F*100:.2f}% = {sn:.0f}bp per year.\n3. Daily: {sn/np.sqrt(252):.1f}bp. "
             f"Structural sellers of vol: callable issuers' investors, MBS holders (short convexity), structured-note "
             f"buyers. Structural buyers: mortgage servicers/hedgers, liability hedgers buying receivers.")
    return Question("rates", "2F", "advanced:normal_vol", d, "f_nvol", seed,
                    prompt=f"A 1y10y swaption is quoted at {sb*100:.0f}% lognormal (Black) vol with the forward at {F*100:.2f}%. Roughly what is the normal vol in bp?",
                    parts=[Part("numeric", "Normal vol (bp/yr)", correct=sn, tol_rel=0.05, unit="bp")],
                    free_text_prompt="Who is structurally long or short rates vol?",
                    facts={"forward": F, "black_vol": sb, "normal_vol_bp": sn}, model_answer=model,
                    rubric=["sigma_N ~ sigma_B x F", "Structural sellers and buyers of vol"])


def f_krd(rng, d, seed):
    c = base_curve()
    m = int(rng.choice([7, 12, 20]))
    b = Bond(0.045, m, 100e6)
    pillars = [2, 5, 10, 20, 30]
    kr = key_rate_dv01s(b.pv, c, pillars)
    big = max(kr, key=lambda k: kr[k])
    names = [f"{p}y" for p in pillars]
    model = (f"**Mostly {big}y.**\n\n1. Key-rate DV01 bumps one pillar at a time (triangular bumps) and reprices. "
             f"It shows WHERE on the curve your duration sits.\n2. A {m}y bond's cash flows sit up to {m}y, so its "
             f"risk lands in the pillars bracketing {m}y: " + ", ".join(f"{k}y {fmt_ccy(v)}" for k, v in kr.items()) +
             f".\n3. The KR DV01s add up to the parallel DV01 ({fmt_ccy(sum(kr.values()))}).")
    return Question("rates", "2F", "advanced:krd", d, "f_krd", seed,
                    prompt=f"You own GBP 100m of a 4.5% {m}y gilt. Which key-rate bucket carries the largest DV01?",
                    parts=[Part("mcq", "Largest bucket", names, pillars.index(big))],
                    free_text_prompt="What does key-rate DV01 tell you that parallel DV01 doesn't?",
                    facts={"key_rate_dv01": kr}, model_answer=model, rubric=["Triangular bumps", "Bracketing pillars", "Sum = parallel"],
                    charts=[chart_bar("Key-rate DV01 (GBP per bp)", names, list(kr.values()), "GBP")])


CONCEPTS = [
    ("advanced:swap_spreads", "Why can swap spreads (swap rate minus government yield) be negative, as in 30y USD?",
     ["Balance-sheet and capital costs make it expensive for dealers to hold bonds, while heavy government supply and demand to receive fixed (e.g. pension liability hedging) pushes swap rates below yields",
      "Because swaps carry more credit risk than government bonds",
      "Because the floating leg of a swap pays a higher rate than repo",
      "Negative spreads are an arbitrage that is always closed immediately"],
     "Swap spreads are not a pure credit spread any more. Holding bonds uses dealer balance sheet (leverage ratio, capital), repo financing is not free, and heavy bond supply cheapens bonds. Meanwhile long-dated receivers (pensions, insurers) push swap rates down. The 'arbitrage' of buying the bond and paying fixed needs balance sheet that is scarce."),
    ("advanced:fly", "Why weight a 2s5s10s butterfly using PCA rather than 50/50 DV01 weights?",
     ["PCA weights neutralise the trade to the level and slope factors as they actually move historically, so the P&L isolates curvature",
      "DV01 weights are always wrong",
      "PCA weights make the trade cheaper to execute",
      "PCA weights maximise carry"],
     "A DV01-neutral 50/50 fly is hedged to parallel moves but not to slope: if the curve steepens, the wings move differently and you get slope P&L. PCA (or regression) weights use how the 2y, 5y and 10y historically co-move, hedging both level and slope so you are left with the curvature view."),
    ("advanced:ldi_2022", "In September 2022, why did UK LDI funds sell gilts as gilt yields spiked?",
     ["They held leveraged long-duration positions (receivers/repo-funded gilts); rising yields triggered collateral calls they met by selling gilts, which pushed yields higher still until the BoE stepped in",
      "They wanted to buy cheap gilts but ran out of time",
      "They were short duration and took profit",
      "Regulation forced them to switch from gilts to equities"],
     "Pension LDI funds hedge long liabilities with leveraged long duration (receive-fixed swaps, repo-funded gilts). The mini-budget sent long gilt yields up very fast. The hedges lost value and needed collateral within days; funds sold their most liquid asset, long gilts, into a falling market: forced selling of duration, a doom loop. The BoE bought long gilts temporarily to break it."),
    ("advanced:delivery_option", "Why do bond futures usually trade cheap to the forward price of the CTD?",
     ["The short owns delivery options (which bond, when to deliver), and the futures price is reduced by their value",
      "Futures have no carry",
      "Futures are more liquid so they trade rich",
      "The long can choose which bond to receive"],
     "The short chooses the bond (switch option) and the timing within the delivery month. Those options have value to the short, so the long pays less: futures trade below the CTD forward / CF, i.e. the net basis is positive and equals the option value at fair pricing."),
]


def f_concept(rng, d, seed):
    topic, q, opts, why = CONCEPTS[int(rng.integers(len(CONCEPTS)))]
    order = rng.permutation(len(opts))
    o = [opts[i] for i in order]
    correct = int(np.where(order == 0)[0][0])
    return Question("rates", "2F", topic, d, "f_concept", seed, prompt=q,
                    parts=[Part("mcq", "Answer", o, correct)], free_text_prompt="Explain in your own words.",
                    facts={"answer": opts[0]}, model_answer=f"**{opts[0]}.**\n\n{why}", rubric=[opts[0], why])


TOPICS = {
    "2B": ("Convexity intuition", [b_barbell, b_maturity_squared, b_long_convexity_cost, b_mortgage]),
    "2C": ("Curve trades", [c_label, c_sizing, c_boe_view]),
    "2D": ("Carry and roll-down", [d_carry_roll]),
    "2E": ("Pricing central banks", [e_probability, e_reaction]),
    "2F": ("Advanced", [f_ctd, f_normal_vol, f_krd, f_concept, f_concept]),
}


def make_generator(code: str):
    fns = TOPICS[code][1]

    def gen(seed: int, difficulty: int) -> Question:
        rng = np.random.default_rng(seed)
        return fns[int(rng.integers(len(fns)))](rng, difficulty, seed)
    return gen

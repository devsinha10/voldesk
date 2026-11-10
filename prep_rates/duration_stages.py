"""Section 2A: who is long duration or convexity? Five unlockable stages.
All P&L and risk numbers are full revaluations on the engine's zero curve."""
from __future__ import annotations

import numpy as np

from engine.config import load_config
from engine.rates import bond_risk, conversion_factor, par_swap_rate
from grading.question import Part, Question, chart_bar, chart_line
from prep_rates.instruments import (FRN, Bond, BondFuture, Composite, Swap, Swaption, base_curve,
                                    callable_bond, fmt_ccy, move_curve, pnl, risk, sign_word)

DUR_OPTS = ["Long duration", "Short duration", "Roughly no duration"]
NVOL = load_config()["rates_engine"]["swaption_normal_vol_bp"] / 1e4


def _dur_index(dv01: float, ref: float) -> int:
    return 2 if abs(dv01) < 0.05 * abs(ref) else (0 if dv01 > 0 else 1)


def _pnl_profile(inst, curve, title: str, ccy: str = "GBP") -> dict:
    moves = np.arange(-150, 151, 25)
    return chart_line(title, moves, {"P&L": [pnl(inst, curve, curve.shifted(m)) for m in moves]},
                      "Parallel move (bp)", f"P&L ({ccy})", vline=0, vline_label="today")


def _move_text(bp: float) -> str:
    return f"yields {'rise' if bp > 0 else 'fall'} {abs(bp):.0f}bp (parallel)"


# ---------------------------------------------------------------------------
# Stage 1: government bonds
# ---------------------------------------------------------------------------
def s1_identify(rng, d, seed):
    c = base_curve()
    mat = int(rng.choice([2, 5, 10, 30]))
    cpn = float(rng.choice([0.0, 0.01, 0.04, 0.0475]))
    side = int(rng.choice([1, -1]))
    face = 100e6
    b = Bond(cpn, mat, side * face)
    r = risk(b, c)
    bp = float(rng.choice([10, 25, 50, 100]) * rng.choice([1, -1]))
    p = pnl(b, c, c.shifted(bp))
    lin = -r.dv01 * bp
    tol = 0.15 if d == 1 else 0.04
    name = f"{'zero-coupon' if cpn == 0 else f'{cpn*100:.2f}%'} {mat}y gilt"
    model = (f"**{DUR_OPTS[_dur_index(r.dv01, face*1e-4)]}; P&L {fmt_ccy(p)}.**\n\n"
             f"1. Intuition: a bond pays fixed cash flows. When yields rise those cash flows are discounted more, so "
             f"the price falls. Owning it means you gain when yields fall: long duration. Being short flips that.\n"
             f"2. DV01 = {fmt_ccy(r.dv01)} per bp (positive = long duration).\n"
             f"3. First-order P&L = -DV01 x move = {fmt_ccy(lin)}. Convexity adds {fmt_ccy(p - lin)} "
             f"(it always helps a long bond and hurts a short one).\n"
             f"4. Full revaluation: {fmt_ccy(p)}.")
    return Question("rates", "2A-1", "duration:bond_basics", d, "s1_identify", seed,
                    prompt=f"You are **{'long' if side > 0 else 'short'} GBP 100m face of a {name}**. "
                           f"Are you long or short duration? What is your P&L if {_move_text(bp)}?",
                    parts=[Part("mcq", "Duration", DUR_OPTS, _dur_index(r.dv01, face * 1e-4)),
                           Part("numeric", "P&L (GBP thousands)", correct=p / 1e3,
                                tol_abs=max(5.0, tol * abs(p / 1e3)), unit="k")],
                    free_text_prompt="Explain the sign and how you sized the P&L.",
                    facts={"bond": name, "side": side, "dv01": r.dv01, "move_bp": bp, "pnl_full": p,
                           "pnl_dv01_only": lin, "convexity_part": p - lin},
                    model_answer=model, rubric=["Long bond = long duration (short flips it)",
                                                "P&L ~ -DV01 x dy", "Convexity term sign"],
                    charts=[_pnl_profile(b, c, "P&L vs parallel move")])


def s1_compare(rng, d, seed):
    y = 0.04
    kind = str(rng.choice(["zero_vs_coupon", "maturity", "coupon"]))
    if kind == "zero_vs_coupon":
        m = int(rng.choice([5, 10, 30]))
        A, B = (0.0, m), (0.05, m)
        why = "A zero pays everything at maturity; a coupon bond returns cash earlier, so its weighted-average time (Macaulay duration) is shorter."
    elif kind == "maturity":
        A, B = (0.04, int(rng.choice([2, 5]))), (0.04, int(rng.choice([10, 30])))
        why = "Cash flows further away are discounted over more years, so their PV reacts more to yield. Longer maturity, more duration."
    else:
        m = int(rng.choice([10, 30]))
        A, B = (0.01, m), (0.06, m)
        why = "A lower coupon puts relatively more of the value in the final principal payment, which pushes the weighted-average time out."
    if rng.random() < 0.5:
        A, B = B, A
    rA, rB = bond_risk(y, *A), bond_risk(y, *B)
    nm = lambda x: f"{'zero' if x[0] == 0 else f'{x[0]*100:.0f}%'} {x[1]}y"
    correct = 0 if rA.modified > rB.modified else 1
    model = (f"**{['A', 'B'][correct]} ({nm([A, B][correct])}) has more duration.**\n\n1. {why}\n"
             f"2. Engine at a {y*100:.0f}% yield: A modified duration {rA.modified:.2f}, B {rB.modified:.2f} "
             f"(Macaulay {rA.macaulay:.2f} vs {rB.macaulay:.2f}).\n3. Rule: duration rises with maturity and falls with "
             f"coupon and yield. A zero's Macaulay duration equals its maturity.")
    return Question("rates", "2A-1", "duration:drivers", d, "s1_compare", seed,
                    prompt=f"Which has more duration? A: **{nm(A)}** bond. B: **{nm(B)}** bond (same yield).",
                    parts=[Part("mcq", "More duration", ["A", "B"], correct)], free_text_prompt="Why?",
                    facts={"A": nm(A), "B": nm(B), "modA": rA.modified, "modB": rB.modified},
                    model_answer=model, rubric=[why],
                    charts=[chart_bar("Modified duration", ["A", "B"], [rA.modified, rB.modified], "years")])


def s1_convexity(rng, d, seed):
    c = base_curve()
    m = int(rng.choice([10, 30]))
    b = Bond(0.04, m, 100e6)
    bp = int(rng.choice([75, 100, 150]))
    up, dn = pnl(b, c, c.shifted(bp)), pnl(b, c, c.shifted(-bp))
    asym = up + dn
    model = (f"**The rally gain ({fmt_ccy(dn)}) is bigger than the selloff loss ({fmt_ccy(up)}).**\n\n"
             f"1. Intuition: the price/yield curve of a vanilla bond bends upwards (positive convexity). As yields fall "
             f"duration lengthens, so you gain at an increasing rate; as yields rise duration shortens, so losses slow.\n"
             f"2. Difference = {fmt_ccy(asym)} = roughly C x P x dy^2 (twice the 0.5 C P dy^2 term).\n"
             f"3. It is the bond-market twin of long gamma: big moves either way help you.")
    return Question("rates", "2A-1", "convexity:bond_basics", d, "s1_convexity", seed,
                    prompt=(f"You own GBP 100m of a 4% {m}y gilt. Compare your P&L if yields fall {bp}bp vs rise "
                            f"{bp}bp. Which is larger in size, and by how much (gain + loss)?"),
                    parts=[Part("mcq", "Larger in size", ["The gain from yields falling", "The loss from yields rising",
                                                          "They are equal"], 0),
                           Part("numeric", "Gain + loss (GBP thousands)", correct=asym / 1e3,
                                tol_abs=max(5.0, 0.12 * abs(asym / 1e3)), unit="k")],
                    free_text_prompt="Explain why.",
                    facts={"bond": f"4% {m}y", "pnl_down": dn, "pnl_up": up, "asymmetry": asym, "move_bp": bp},
                    model_answer=model, rubric=["Positive convexity", "Gain > loss", "Duration lengthens as yields fall"],
                    charts=[_pnl_profile(b, c, "Long bond: P&L vs parallel move (curved = convexity)")])


# ---------------------------------------------------------------------------
# Stage 2: futures and repo
# ---------------------------------------------------------------------------
def s2_future(rng, d, seed):
    c = base_curve()
    ctd = Bond(0.0425, 9, 100e3)  # one contract = GBP 100k face
    cf = conversion_factor(0.0425, 9, notional_coupon=0.04)
    n = int(rng.choice([200, 500, 1000])) * int(rng.choice([1, -1]))
    fut = Composite([BondFuture(Bond(0.0425, 9, 100e3 * n), cf, c)], name="futures")
    r = risk(fut, c)
    bp = float(rng.choice([5, 10, 20]) * rng.choice([1, -1]))
    p = pnl(fut, c, c.shifted(bp))
    per = risk(BondFuture(ctd, cf, c), c).dv01
    model = (f"**{DUR_OPTS[_dur_index(r.dv01, 1)]}; P&L {fmt_ccy(p)}.**\n\n"
             f"1. A bond future tracks the cheapest-to-deliver bond divided by its conversion factor, so long futures "
             f"behave like long bonds: long duration, with no cash outlay (it is leveraged duration).\n"
             f"2. DV01 per contract ~ DV01(CTD per 100k) / CF = {fmt_ccy(per)} (CF {cf:.4f}).\n"
             f"3. Position DV01 = {fmt_ccy(r.dv01)}; P&L ~ -DV01 x {bp:+.0f} = {fmt_ccy(p)}.")
    return Question("rates", "2A-2", "duration:futures", d, "s2_future", seed,
                    prompt=(f"You are **{'long' if n > 0 else 'short'} {abs(n)} Long Gilt futures** (GBP 100k face each, "
                            f"CTD 4.25% 9y gilt). Long or short duration? P&L if {_move_text(bp)}?"),
                    parts=[Part("mcq", "Duration", DUR_OPTS, _dur_index(r.dv01, 1)),
                           Part("numeric", "P&L (GBP thousands)", correct=p / 1e3, tol_abs=max(2.0, 0.08 * abs(p / 1e3)))],
                    free_text_prompt="Explain the link between futures and the CTD.",
                    facts={"contracts": n, "cf": cf, "dv01_per_contract": per, "dv01": r.dv01, "move_bp": bp, "pnl": p},
                    model_answer=model, rubric=["Long futures = long duration", "DV01 = CTD DV01 / CF", "Leveraged"])


def s2_repo(rng, d, seed):
    c = base_curve()
    m = int(rng.choice([5, 10, 30]))
    cpn = float(rng.choice([0.0425, 0.045, 0.0475]))
    face = 100e6
    b = Bond(cpn, m, face)
    P = b.pv(c)
    repo = float(rng.choice([0.035, 0.0375, 0.04, 0.045, 0.05]))
    h = 0.25
    carry = cpn * face * h - P * repo * h
    r = risk(b, c)
    be = carry / r.dv01
    model = (f"**Carry {fmt_ccy(carry)} over 3 months ({'positive' if carry > 0 else 'negative'}).**\n\n"
             f"1. You buy the bond and borrow the cash in repo, pledging the bond. You earn the coupon accrual and pay "
             f"the repo rate on the cash borrowed.\n2. Coupon: {cpn*100:.2f}% x {face/1e6:.0f}m x 0.25 = "
             f"{fmt_ccy(cpn*face*h)}. Repo: {repo*100:.2f}% x {fmt_ccy(P).lstrip('+')} x 0.25 = {fmt_ccy(-P*repo*h)}.\n"
             + (f"3. Breakeven: yields can rise about {be:.1f}bp over the period before the price loss "
                f"(DV01 {fmt_ccy(r.dv01)}) wipes out the carry. " if carry > 0 else
                f"3. Negative carry: yields must FALL about {abs(be):.1f}bp over the period (DV01 {fmt_ccy(r.dv01)}) "
                f"just to pay for the funding. ") +
             f"Carry is to bonds what theta is to options.\n"
             f"4. Duration is still long: repo funding changes the cash outlay, not the rate risk.")
    return Question("rates", "2A-2", "duration:repo_carry", d, "s2_repo", seed,
                    prompt=(f"You buy GBP 100m of a {cpn*100:.2f}% {m}y gilt (dirty price ~{P/face*100:.2f}) and fund it "
                            f"in 3-month repo at {repo*100:.2f}%. What is your carry over 3 months (ignore pull-to-par)? "
                            f"Are you still long duration?"),
                    parts=[Part("numeric", "Carry (GBP thousands)", correct=carry / 1e3, tol_abs=max(3.0, 0.05 * abs(carry / 1e3))),
                           Part("mcq", "Duration", DUR_OPTS, 0)],
                    free_text_prompt="Explain the carry and the breakeven.",
                    facts={"price": P, "coupon": cpn, "repo": repo, "carry": carry, "dv01": r.dv01, "breakeven_bp": be},
                    model_answer=model, rubric=["Carry = coupon - repo cost", "Breakeven = carry / DV01",
                                                "Still long duration"])


# ---------------------------------------------------------------------------
# Stage 3: swaps
# ---------------------------------------------------------------------------
def s3_swap(rng, d, seed):
    c = base_curve()
    T = int(rng.choice([2, 5, 10, 30]))
    direction = str(rng.choice(["receive", "pay"]))
    K = par_swap_rate(c, 0, T)
    sw = Swap(0, T, K, 100e6, direction)
    r = risk(sw, c)
    bp = float(rng.choice([10, 25, 50]) * rng.choice([1, -1]))
    p = pnl(sw, c, c.shifted(bp))
    model = (f"**{DUR_OPTS[_dur_index(r.dv01, 1)]}; P&L {fmt_ccy(p)}.**\n\n"
             f"1. Receiving fixed = owning a fixed-rate bond funded at the floating rate: you gain when rates fall, "
             f"so you are long duration. Paying fixed is the opposite (short duration).\n"
             f"2. The floating leg resets to market, so it has almost no duration; all the DV01 sits in the fixed leg: "
             f"DV01 ~ notional x annuity x 1bp = {fmt_ccy(r.dv01)}.\n3. P&L for {bp:+.0f}bp: {fmt_ccy(p)}.")
    return Question("rates", "2A-3", "duration:swaps", d, "s3_swap", seed,
                    prompt=(f"You **{direction} fixed** on GBP 100m of a {T}y SONIA swap at par ({K*100:.3f}%). "
                            f"Long or short duration? P&L if {_move_text(bp)}?"),
                    parts=[Part("mcq", "Duration", DUR_OPTS, _dur_index(r.dv01, 1)),
                           Part("numeric", "P&L (GBP thousands)", correct=p / 1e3, tol_abs=max(3.0, 0.06 * abs(p / 1e3)))],
                    free_text_prompt="Explain with the bond analogy.",
                    facts={"tenor": T, "direction": direction, "par_rate": K, "dv01": r.dv01, "move_bp": bp, "pnl": p},
                    model_answer=model, rubric=["Receive fixed = long duration", "Bond funded at floating analogy",
                                                "Floating leg has ~no duration"],
                    charts=[_pnl_profile(sw, c, "Swap P&L vs parallel move")])


def s3_floater(rng, d, seed):
    c = base_curve()
    T = int(rng.choice([5, 10]))
    frn = FRN(100e6, 0.25, c.fwd(0, 0.25))
    fixed = Bond(par_swap_rate(c, 0, T), T, 100e6, freq=1)
    rf, rb = risk(frn, c), risk(fixed, c)
    opts = ["The floating-rate note has almost no duration (only until its next reset)",
            "Both have similar duration", "The floater has more duration because its coupon rises with rates"]
    model = (f"**{opts[0]}.**\n\n1. A floater's coupon resets to the market rate every period, so after each reset it "
             f"is worth about par whatever rates did. Its only rate risk is the current fixed coupon until the next "
             f"reset (3 months here).\n2. Engine DV01s: FRN {fmt_ccy(rf.dv01)} vs {T}y fixed bond {fmt_ccy(rb.dv01)} "
             f"(ratio {rf.dv01 / rb.dv01:.3f}).\n3. This is why the floating leg of a swap carries almost no duration.")
    return Question("rates", "2A-3", "duration:floaters", d, "s3_floater", seed,
                    prompt=f"Compare GBP 100m of a {T}y SONIA floating-rate note (next reset in 3 months) with GBP 100m of a {T}y fixed bond.",
                    parts=[Part("mcq", "Duration", opts, 0)], free_text_prompt="Why?",
                    facts={"dv01_frn": rf.dv01, "dv01_fixed": rb.dv01}, model_answer=model,
                    rubric=["Floater resets to market", "Duration ~ time to next reset"],
                    charts=[chart_bar("DV01 (GBP per bp)", ["FRN", f"{T}y fixed"], [rf.dv01, rb.dv01], "GBP")])


def s3_forward(rng, d, seed):
    from engine.rates import key_rate_dv01s
    c = base_curve()
    s, L = rng.choice([(2, 3), (5, 5), (1, 4)])
    s, L = int(s), int(L)
    K = par_swap_rate(c, s, s + L)
    sw = Swap(s, s + L, K, 100e6, "receive")
    pillars = [1, 2, 3, 5, 7, 10, 20]
    kr = key_rate_dv01s(sw.pv, c, pillars)
    big = max(kr, key=lambda k: kr[k])
    small = min(kr, key=lambda k: kr[k])
    opts = [f"Long duration around {s + L}y, short duration around {s}y",
            f"Long duration at all tenors up to {s + L}y",
            f"Short duration around {s + L}y, long around {s}y",
            "No duration until the swap starts"]
    model = (f"**{opts[0]}.**\n\n1. A forward-starting receiver = receive fixed on a {s + L}y swap and pay fixed on a {s}y "
             f"swap. Nothing is exchanged before year {s}, so the near cash flows cancel.\n2. Key-rate DV01s: " +
             ", ".join(f"{k}y {fmt_ccy(v)}" for k, v in kr.items()) +
             f".\n3. Net DV01 {fmt_ccy(sum(kr.values()))}: long duration overall, concentrated at {big}y, with a short "
             f"at {small}y. It is a pure bet on the {s}y{L}y forward rate.")
    return Question("rates", "2A-3", "duration:forward_swaps", d, "s3_forward", seed,
                    prompt=f"You receive fixed on GBP 100m of a **{s}y{L}y forward-starting swap** at {K*100:.3f}%. Describe your duration exposure along the curve.",
                    parts=[Part("mcq", "Exposure", opts, 0)], free_text_prompt="Explain.",
                    facts={"key_rate_dv01": kr, "start": s, "length": L}, model_answer=model,
                    rubric=["Equivalent to long (s+L)y receiver, short sy receiver", "Long the forward rate"],
                    charts=[chart_bar("Key-rate DV01 (GBP per bp)", [f"{k}y" for k in kr], list(kr.values()), "GBP")])


# ---------------------------------------------------------------------------
# Stage 4: swaptions
# ---------------------------------------------------------------------------
def _swaption(c, kind, side, exp=1.0, ten=10.0, n=100e6, k_off_bp=0.0):
    F = par_swap_rate(c, exp, exp + ten)
    return Swaption(exp, ten, F + k_off_bp * 1e-4, NVOL, kind, side * n)


def s4_signs(rng, d, seed):
    c = base_curve()
    kind = str(rng.choice(["payer", "receiver"]))
    side = int(rng.choice([1, -1]))
    exp, ten = (1.0, 10.0) if d == 1 else (float(rng.choice([0.5, 1, 2])), float(rng.choice([5, 10])))
    sw = _swaption(c, kind, side, exp, ten)
    r = risk(sw, c)
    ref = risk(_swaption(c, "receiver", 1, exp, ten), c)
    corr = {"Duration": sign_word(r.dv01, ref.dv01), "Convexity": sign_word(r.convexity_pnl, ref.convexity_pnl)}
    model = (f"**Duration {corr['Duration']}, convexity {corr['Convexity']}.**\n\n"
             f"1. A receiver swaption is the right to receive fixed: it gains when rates fall, so it is long duration. "
             f"A payer is the right to pay fixed: short duration.\n2. Any LONG option is long convexity (long gamma): "
             f"its duration grows in the direction that makes money. SHORT either one and you are short convexity.\n"
             f"3. Engine: DV01 {fmt_ccy(r.dv01)}; P&L of +/-25bp combined {fmt_ccy(r.convexity_pnl)}; DV01 at +50bp "
             f"{fmt_ccy(r.dv01_up50)}, at -50bp {fmt_ccy(r.dv01_dn50)}.")
    return Question("rates", "2A-4", "convexity:swaptions", d, "s4_signs", seed,
                    prompt=(f"You are **{'long' if side > 0 else 'short'} GBP 100m of {exp:g}y-into-{ten:g}y ATM "
                            f"{kind} swaptions** (normal vol {NVOL*1e4:.0f}bp). Fill in your exposures."),
                    parts=[Part("sign_table", "Exposure", rows=["Duration", "Convexity"], correct=corr)],
                    free_text_prompt="Explain each sign.",
                    facts={"kind": kind, "side": side, "dv01": r.dv01, "convexity_pnl_25bp": r.convexity_pnl,
                           "dv01_up50": r.dv01_up50, "dv01_dn50": r.dv01_dn50}, model_answer=model,
                    rubric=["Receiver long duration / payer short", "Long option = long convexity", "Short option = short convexity"],
                    charts=[_pnl_profile(sw, c, "Swaption P&L vs parallel move")])


def s4_delta_change(rng, d, seed):
    c = base_curve()
    kind = str(rng.choice(["payer", "receiver"]))
    sw = _swaption(c, kind, 1)
    bp = float(rng.choice([25, 50, 75]) * rng.choice([1, -1]))
    r0 = risk(sw, c)
    r1 = risk(sw, c.shifted(bp))
    grew = abs(r1.dv01) > abs(r0.dv01)
    opts = ["It grows in size", "It shrinks in size", "It stays the same"]
    model = (f"**{opts[0 if grew else 1]}: DV01 {fmt_ccy(r0.dv01)} to {fmt_ccy(r1.dv01)}.**\n\n"
             f"1. Swaption 'delta' (its DV01) behaves like an option delta: as the forward swap rate moves "
             f"{'into' if (bp > 0) == (kind == 'payer') else 'out of'} the money, the delta "
             f"{'grows towards' if grew else 'shrinks towards'} {'a full swap' if grew else 'zero'}.\n"
             f"2. Because you are long the option, your duration always moves in your favour: long convexity.\n"
             f"3. To stay hedged you would {'pay' if r1.dv01 - r0.dv01 > 0 else 'receive'} more fixed in swaps.")
    return Question("rates", "2A-4", "convexity:swaption_delta", d, "s4_delta", seed,
                    prompt=f"You are long GBP 100m 1y-into-10y ATM **{kind}** swaptions. Rates move {bp:+.0f}bp. What happens to the size of your duration exposure?",
                    parts=[Part("mcq", "Duration exposure", opts, 0 if grew else 1),
                           Part("numeric", "New DV01 (GBP thousands)", correct=r1.dv01 / 1e3, tol_abs=max(1.0, 0.1 * abs(r1.dv01 / 1e3)))],
                    free_text_prompt="Explain using the option analogy.",
                    facts={"dv01_before": r0.dv01, "dv01_after": r1.dv01, "move_bp": bp, "kind": kind},
                    model_answer=model, rubric=["Delta of swaption changes like option delta", "Long convexity"])


# ---------------------------------------------------------------------------
# Stage 5: mixed books
# ---------------------------------------------------------------------------
LOGIC = {
    "rec_plus_payer": ("Receiving 10y is long duration with ~no convexity; the long payers are short duration and long "
                       "convexity. In a selloff the payers' delta grows and offsets more of the swap loss; in a rally "
                       "they fade and the receiver's gains dominate. Net: the payers cap the downside of the receiver."),
    "bond_plus_short_receiver": ("Selling receivers adds long duration that grows as rates fall (the option goes in "
                                 "the money) and disappears as rates rise: you are short convexity, paid for with "
                                 "premium. It is the same shape as owning a callable bond or MBS."),
    "callable": ("A callable bond is a bullet bond minus the issuer's call (a receiver swaption you are short). When "
                 "rates fall the bond gets called, so its duration shortens exactly when you want more of it: long "
                 "duration, short convexity, like MBS."),
    "payer_hedged": ("A delta-hedged long payer starts flat duration but long convexity. After a selloff the payer's "
                     "delta grows, so you end up short duration (you make money on the move); after a rally you end up "
                     "long duration. Either way the move pays you: that is long gamma in rates."),
}


def s5_book(rng, d, seed):
    c = base_curve()
    variant = str(rng.choice(["rec_plus_payer", "bond_plus_short_receiver", "callable", "payer_hedged"]))
    if variant == "rec_plus_payer":
        K = par_swap_rate(c, 0, 10)
        sw = Swap(0, 10, K, 100e6, "receive")
        opt = _swaption(c, "payer", 1, 2.0, 10.0, n=float(rng.choice([50e6, 100e6])))
        book = Composite([sw, opt])
        desc = (f"The desk **receives fixed on GBP 100m 10y** at {K*100:.3f}% and is **long GBP {opt.notional/1e6:.0f}m "
                f"2y-into-10y ATM payer swaptions**.")
    elif variant == "bond_plus_short_receiver":
        b = Bond(0.045, 10, 100e6)
        opt = _swaption(c, "receiver", -1, 1.0, 9.0, 100e6, -25)
        book = Composite([b, opt])
        desc = "The desk owns **GBP 100m of a 4.5% 10y gilt** and has **sold GBP 100m 1y-into-9y receiver swaptions** 25bp out of the money (to earn premium)."
    elif variant == "callable":
        book = callable_bond(0.045, 10, 2, 100e6, NVOL, c)
        desc = "The desk owns **GBP 100m of a 4.5% 10y callable bond** (issuer can call at par in 2 years). Think of it like an MBS."
    else:
        opt = _swaption(c, "payer", 1, 1.0, 10.0)
        r_opt = risk(opt, c)
        sw = Swap(0, 10, par_swap_rate(c, 0, 10), abs(r_opt.dv01) / risk(Swap(0, 10, par_swap_rate(c, 0, 10), 1.0), c).dv01, "receive")
        book = Composite([opt, sw])
        desc = "The desk is **long GBP 100m 1y-into-10y ATM payer swaptions, delta-hedged by receiving fixed in 10y swaps**."
    bp = float(rng.choice([50, 75, -50, -75]))
    moved = c.shifted(bp)
    p = pnl(book, c, moved)
    r0, r1 = risk(book, c), risk(book, moved)
    ref = 100e6 * 1e-4 * 5
    corr = {"Duration": sign_word(r1.dv01, ref), "Convexity": sign_word(r1.convexity_pnl, risk(_swaption(c, 'receiver', 1), c).convexity_pnl)}
    comp = [(getattr(x, "name", "leg"), pnl(x, c, moved)) for x in book.parts]
    model = (f"**P&L {fmt_ccy(p)}; after the move duration {corr['Duration']}, convexity {corr['Convexity']}.**\n\n"
             f"1. Component P&L: " + ", ".join(f"{n} {fmt_ccy(v)}" for n, v in comp) + ".\n"
             f"2. Risk before: DV01 {fmt_ccy(r0.dv01)}, convexity (+/-25bp) {fmt_ccy(r0.convexity_pnl)}. After: DV01 "
             f"{fmt_ccy(r1.dv01)}, convexity {fmt_ccy(r1.convexity_pnl)}.\n"
             f"3. Logic: {LOGIC[variant]}\n"
             f"4. Hedging: re-hedge the DV01 change with swaps or futures; if you are short convexity, every re-hedge "
             f"is 'buy high, sell low'.")
    return Question("rates", "2A-5", "mixed:books", d, f"s5_{variant}", seed,
                    prompt=f"{desc}\n\nRates move **{bp:+.0f}bp** in parallel. Walk through your P&L and how your risk has changed.",
                    parts=[Part("numeric", "Total P&L (GBP thousands)", correct=p / 1e3, tol_abs=max(5.0, 0.1 * abs(p / 1e3))),
                           Part("sign_table", "Exposure after the move", rows=["Duration", "Convexity"], correct=corr)],
                    free_text_prompt="Walk through the P&L by component and the change in risk.",
                    facts={"variant": variant, "move_bp": bp, "pnl_total": p, "components": comp,
                           "dv01_before": r0.dv01, "dv01_after": r1.dv01, "convexity_before": r0.convexity_pnl,
                           "convexity_after": r1.convexity_pnl}, model_answer=model,
                    rubric=["P&L by component", "Duration change after the move", "Convexity sign and why"],
                    charts=[_pnl_profile(book, c, "Book P&L vs parallel move")])


STAGES = {
    "2A-1": ("Stage 1: Government bonds", [s1_identify, s1_compare, s1_convexity]),
    "2A-2": ("Stage 2: Bond futures and repo", [s2_future, s2_repo]),
    "2A-3": ("Stage 3: Swaps", [s3_swap, s3_floater, s3_forward]),
    "2A-4": ("Stage 4: Swaptions", [s4_signs, s4_delta_change]),
    "2A-5": ("Stage 5: Mixed books", [s5_book]),
}


def make_generator(stage: str):
    fns = STAGES[stage][1]

    def gen(seed: int, difficulty: int) -> Question:
        rng = np.random.default_rng(seed)
        return fns[int(rng.integers(len(fns)))](rng, difficulty, seed)
    return gen

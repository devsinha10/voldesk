"""Section 1C: no-arbitrage, implied vs realised, gamma/theta, skew, sticky
strike vs sticky delta, and trade expression. Numbers from the engine."""
from __future__ import annotations

import numpy as np

from engine.fx_conventions import TENORS
from engine.fx_pricer import price
from engine.pnl_attribution import attribute_legs
from engine.structures import build, flat_market
from grading.question import Part, Question, chart_bar, chart_line
from prep_options.common import fmt_num, fx_market, pick_pair, static_market


# ---------------------------------------------------------------------------
# No-arbitrage
# ---------------------------------------------------------------------------
def q_arbitrage(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    variants = ["call_spread"] + (["put_spread", "butterfly", "calendar"] if difficulty >= 2 else []) + \
               (["parity"] if difficulty >= 2 else [])
    v = str(rng.choice(variants))
    S, r, sig = 100.0, 0.0, float(rng.choice([0.15, 0.2, 0.25]))
    T = float(rng.choice([0.25, 0.5, 1.0]))
    rates_txt = "Assume zero interest rates and no dividends."
    if v in ("call_spread", "put_spread"):
        K1 = float(rng.choice([95, 100, 105]))
        w = float(rng.choice([5, 10]))
        K2 = K1 + w
        p = round(w + float(rng.choice([0.5, 1.0, 1.5])), 2)
        kind = "call" if v == "call_spread" else "put"
        legs = f"{K1:.0f}/{K2:.0f} {kind} spread ({'long' if kind=='call' else 'short'} the {K1:.0f}, {'short' if kind=='call' else 'long'} the {K2:.0f})"
        prompt = f"A {T:g}y {legs} trades at **{p:.2f}**. {rates_txt} What do you do?"
        opts = ["Sell the spread: its payoff can never exceed the strike width, so you lock in the excess",
                "Buy the spread: it is cheap relative to the width",
                "Nothing: the price is within no-arbitrage bounds",
                "Buy the lower strike option outright"]
        correct = 0
        profit = p - w
        model = (f"**Sell the spread.** 1) Intuition: a {kind} spread pays between 0 and the strike width "
                 f"({w:.0f}). Paying more than {w:.0f} today (more than PV of {w:.0f} with rates) guarantees a loss "
                 f"for the buyer. 2) Sell it at {p:.2f}, worst case you pay {w:.0f} at expiry: locked-in profit "
                 f"at least {profit:.2f}. 3) Bounds: 0 <= spread <= (K2 - K1) e^(-rT).")
        facts = {"price": p, "width": w, "upper_bound": w, "arb_profit_min": profit}
    elif v == "butterfly":
        Ks = [90.0, 100.0, 110.0]
        C = [float(price(S, K, T, r, 0, sig, "C")) for K in Ks]
        bump = round(float(rng.uniform(0.3, 1.0)) + max(C[0] - 2 * C[1] + C[2], 0), 2)
        C[1] = C[1] + bump / 2
        fly = C[0] - 2 * C[1] + C[2]
        prompt = (f"{T:g}y calls on an index at 100 trade at: 90 strike **{C[0]:.2f}**, 100 strike **{C[1]:.2f}**, "
                  f"110 strike **{C[2]:.2f}**. {rates_txt} Is there an arbitrage? What is the trade?")
        opts = ["Buy the 90/100/110 butterfly (buy 90, sell 2x100, buy 110): you get paid to own a non-negative payoff",
                "Sell the butterfly", "No arbitrage", "Buy the 100 call, sell the 90 call"]
        correct = 0
        profit = -fly
        model = (f"**Buy the butterfly for a credit.** 1) A 1x2x1 call fly pays max(0, ...) >= 0 everywhere, so it "
                 f"must cost >= 0. Equivalently call prices must be convex in strike. 2) Price = C90 - 2C100 + C110 = "
                 f"{fly:.2f} < 0, so you receive {-fly:.2f} to own a payoff that is never negative. 3) In vol terms: "
                 f"the 100 strike is too expensive relative to the wings, i.e. the implied density goes negative.")
        facts = {"calls": dict(zip(["90", "100", "110"], C)), "fly_price": fly, "arb_profit_min": profit}
    elif v == "calendar":
        K = 100.0
        T1, T2 = 0.25, 0.5
        c1 = float(price(S, K, T1, 0, 0, sig, "C"))
        c2 = float(price(S, K, T2, 0, 0, sig, "C"))
        c1 = round(c2 + float(rng.uniform(0.2, 0.8)), 2)
        prompt = (f"With spot 100, the 3M 100-strike call trades at **{c1:.2f}** and the 6M 100-strike call at "
                  f"**{c2:.2f}**. {rates_txt} What do you do?")
        opts = ["Sell the 3M call, buy the 6M call (long calendar for a credit)",
                "Buy the 3M call, sell the 6M call", "No arbitrage: shorter options can be worth more",
                "Buy both"]
        correct = 0
        profit = c1 - c2
        model = (f"**Buy the calendar for a credit.** 1) With zero rates and no dividends, a longer-dated European "
                 f"call is worth at least as much as a shorter one at the same strike (total variance must increase "
                 f"with time). 2) Sell 3M at {c1:.2f}, buy 6M at {c2:.2f}: credit {profit:.2f}. At 3M expiry the 6M "
                 f"call is worth at least max(S - K, 0), which covers what you owe on the short. 3) In FX, rates "
                 f"differ, so the clean check is on total implied variance at the same forward moneyness.")
        facts = {"near_call": c1, "far_call": c2, "credit": profit}
    else:  # parity, FX form
        mkt = fx_market("EURUSD")
        T = 0.25
        K = round(mkt.forward(T), 4)
        v_ = mkt.vol(K, T)
        c = float(price(mkt.spot, K, T, mkt.rd, mkt.rf, v_, "C"))
        p = float(price(mkt.spot, K, T, mkt.rd, mkt.rf, v_, "P"))
        mis = float(rng.choice([-1, 1])) * round(float(rng.uniform(8, 25))) * 1e-4
        c_q = c + mis
        prompt = (f"EURUSD spot {mkt.spot:.4f}, 3M USD rate {mkt.rd*100:.2f}%, EUR rate {mkt.rf*100:.2f}% "
                  f"(continuous). The 3M {K:.4f} EUR call trades at **{c_q/1e-4:.0f} USD pips** and the put at "
                  f"**{p/1e-4:.0f} USD pips**. Is put-call parity respected? What is the trade?")
        rhs = mkt.spot * np.exp(-mkt.rf * T) - K * np.exp(-mkt.rd * T)
        lhs = c_q - p
        rich = "call" if lhs > rhs else "put"
        opts = ["Sell the call, buy the put, buy EUR forward (synthetic long forward is cheaper)",
                "Buy the call, sell the put, sell EUR forward",
                "Parity holds: no trade"]
        correct = 0 if rich == "call" else 1
        profit = abs(lhs - rhs)
        model = (f"**{opts[correct]}.** 1) FX parity: C - P = S e^(-rf T) - K e^(-rd T) (a long call + short put is "
                 f"a forward bought at K). 2) Right side = {rhs/1e-4:.1f} pips; market C - P = {lhs/1e-4:.1f} pips, "
                 f"so the {rich} is rich by {profit/1e-4:.1f} pips. 3) Sell the rich side, buy the cheap side and "
                 f"hedge with the forward: profit about {profit/1e-4:.1f} USD pips per EUR.")
        facts = {"C_minus_P": lhs, "S_dff_minus_K_dfd": rhs, "mispricing": profit, "rich_leg": rich}
        profit = profit / 1e-4
    return Question(section="options", subsection="1C", topic=f"concepts:arbitrage", difficulty=difficulty,
                    template=f"arb_{v}", seed=seed, prompt=prompt,
                    parts=[Part("mcq", "Trade", opts, correct),
                           Part("numeric", "Locked-in profit per unit" + (" (pips)" if v == "parity" else ""),
                                correct=float(profit), tol_abs=0.05 if v != "parity" else 1.0)],
                    free_text_prompt="Explain the arbitrage and the bound being violated.",
                    facts=facts, model_answer=model,
                    rubric=["Identifies the violated bound", "Correct direction of trade", "Locked-in profit"])


# ---------------------------------------------------------------------------
# Gamma / theta, implied vs realised
# ---------------------------------------------------------------------------
def q_breakeven(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    pair = pick_pair(rng)
    base = fx_market(pair)
    tenor = str(rng.choice(["1W", "1M", "3M"]))
    tau = TENORS[tenor]
    v = base.vol(base.forward(tau), tau)
    mkt = flat_market(base.pair, base.spot, base.rd, base.rf, v)
    s = build("straddle", mkt, tenor, 1e7)
    e = s.exposure(mkt)
    gamma_unit = e.gamma_1pct / (0.01 * mkt.spot)       # d2V/dS2 for the whole position
    dS = np.sqrt(2 * abs(e.theta) / gamma_unit)
    pct = dS / mkt.spot * 100
    rule = v * 100 / np.sqrt(365)
    model = (f"**About {pct:.2f}% per day ({dS/mkt.pair.pip:,.0f} pips).**\n\n"
             f"1. Intuition: a delta-hedged long option earns 0.5 x gamma x dS^2 from each move and pays theta each "
             f"day. You break even when 0.5 x gamma x dS^2 = |theta|.\n"
             f"2. dS = sqrt(2|theta|/gamma) = sqrt(2 x {abs(e.theta):,.0f} / {gamma_unit:,.0f}) = {dS:.{mkt.pair.decimals}f}.\n"
             f"3. Rule of thumb: theta ~ -0.5 gamma S^2 vol^2 / 365, so the breakeven daily move is about "
             f"vol / sqrt(365) = {v*100:.2f}% / 19.1 = {rule:.2f}%. Realised vol above implied wins, below loses.")
    return Question(section="options", subsection="1C", topic="concepts:gamma_theta", difficulty=difficulty,
                    template="breakeven", seed=seed,
                    prompt=(f"You buy a {tenor} ATM {pair} straddle at {v*100:.2f}% vol and delta-hedge it. Spot is "
                            f"{mkt.spot:.{mkt.pair.decimals}f}. Roughly how big a daily move (in %) do you need to "
                            f"break even on theta?"),
                    parts=[Part("numeric", "Breakeven daily move (%)", correct=float(pct), tol_rel=0.12, unit="%")],
                    free_text_prompt="Explain the gamma/theta trade-off behind your number.",
                    facts={"pair": pair, "vol": v, "theta_per_day": e.theta, "gamma_1pct": e.gamma_1pct,
                           "breakeven_move_pct": pct, "rule_of_thumb_pct": rule},
                    model_answer=model,
                    rubric=["0.5 gamma dS^2 = theta", f"About {pct:.2f}%", "Equivalent to vol/sqrt(365)",
                            "Realised vs implied determines P&L"])


def q_realised_vs_implied(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    pair = pick_pair(rng)
    base = fx_market(pair)
    tau = TENORS["1M"]
    vi = round(base.vol(base.forward(tau), tau) * 100, 1)
    vr = round(vi + float(rng.choice([-3, -2, 2, 3, 4])), 1)
    days = int(rng.choice([5, 10]))
    mkt = flat_market(base.pair, base.spot, base.rd, base.rf, vi / 100)
    s = build("straddle", mkt, "1M", 1e7)
    e = s.exposure(mkt)
    gamma_unit = e.gamma_1pct / (0.01 * mkt.spot)
    pnl = 0.5 * gamma_unit * mkt.spot ** 2 * ((vr / 100) ** 2 - (vi / 100) ** 2) * days / 365
    # simulate a path at exactly the realised vol to show the noise around the formula
    model = (f"**About {fmt_num(pnl)} {mkt.pair.quote}.**\n\n"
             f"1. Intuition: a delta-hedged option's P&L is the gap between the variance you realise and the "
             f"variance you paid for, weighted by cash gamma.\n"
             f"2. Daily P&L ~ 0.5 x Gamma x S^2 x (realised^2 - implied^2) x dt.\n"
             f"3. Here 0.5 x {gamma_unit:,.0f} x {mkt.spot:.4g}^2 x ({vr/100:.3f}^2 - {vi/100:.3f}^2) x {days}/365 = "
             f"{pnl:,.0f}.\n4. Caveats: gamma changes as spot moves and time passes, and the P&L depends on WHEN the "
             f"moves happen (path dependence); this is the constant-gamma estimate.")
    return Question(section="options", subsection="1C", topic="concepts:implied_vs_realised", difficulty=difficulty,
                    template="rv_iv", seed=seed,
                    prompt=(f"You are long a delta-hedged 1M ATM {pair} straddle, {pair[:3]} 10m per leg, bought at "
                            f"{vi:.1f}% implied. Over the next {days} days spot realises {vr:.1f}% vol and implied "
                            f"is unchanged. Roughly what is your P&L (in {mkt.pair.quote}, use today's gamma)?"),
                    parts=[Part("mcq", "Sign of P&L", ["Profit", "Loss"], 0 if pnl > 0 else 1),
                           Part("numeric", f"P&L ({mkt.pair.quote})", correct=float(pnl), tol_rel=0.12)],
                    free_text_prompt="Explain where the P&L comes from.",
                    facts={"pair": pair, "implied": vi, "realised": vr, "days": days, "gamma_1pct": e.gamma_1pct,
                           "gamma_d2V_dS2": gamma_unit, "spot": mkt.spot, "pnl_estimate": pnl, "theta_per_day": e.theta},
                    model_answer=model,
                    rubric=["P&L ~ 0.5 Gamma S^2 (realised^2 - implied^2) dt", "Sign from realised vs implied",
                            "Path dependence / gamma changes"])


def q_straddle_puzzle(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    s = build("straddle", mkt, "1M", 1e7)
    win = rng.random() < 0.5
    if win:
        dv = round(float(rng.uniform(0.8, 2.0)), 1)
        m1 = mkt.pass_time(1).bump_vol(dv)
        prompt = (f"You are long a 1M ATM {pair} straddle. A day later spot is exactly where it was, yet you made "
                  f"money. Why?")
        opts = ["Implied vol rose: the vega gain outweighed one day of theta",
                "Theta is positive for a long straddle", "Gamma: spot must have moved",
                "Rates moved in your favour"]
    else:
        pct = round(float(rng.uniform(0.6, 1.0)), 1)
        dv = -round(float(rng.uniform(1.5, 3.0)), 1)
        m1 = mkt.pass_time(1).bump_spot(pct).bump_vol(dv)
        prompt = (f"You are long a 1M ATM {pair} straddle. A day later spot has moved {pct}%, yet you lost money. "
                  f"Why?")
        opts = ["Implied vol fell: the vega loss (plus theta) outweighed the gamma gain",
                "Long straddles lose when spot moves", "Delta was too long", "Theta was positive"]
    att = attribute_legs(s.legs, mkt, m1)
    t = att.terms
    model = (f"**{opts[0]}.**\n\n1. A long straddle is long gamma, long vega and short theta.\n"
             f"2. Engine attribution: total {fmt_num(att.actual)} = delta {fmt_num(t['delta'])}, gamma "
             f"{fmt_num(t['gamma'])}, vega {fmt_num(t['vega'])}, theta {fmt_num(t['theta'])}, volga "
             f"{fmt_num(t['volga'])}, other {fmt_num(att.unexplained + t['vanna'] + t['rho'])}.\n"
             f"3. Lesson: an option is a bet on both realised and implied vol; the vega leg can dominate a day's P&L.")
    return Question(section="options", subsection="1C", topic="concepts:pnl_explain", difficulty=difficulty,
                    template="straddle_puzzle", seed=seed, prompt=prompt,
                    parts=[Part("mcq", "Main reason", opts, 0)], free_text_prompt="Explain with the Greeks.",
                    facts={"pair": pair, "pnl": att.actual, "attribution": t, "vol_change_pts": dv},
                    model_answer=model, rubric=["Identifies vega as main driver", "Mentions theta and gamma correctly"],
                    charts=[chart_bar("P&L attribution", list(t.keys()), list(t.values()), mkt.pair.quote)])


# ---------------------------------------------------------------------------
# Skew and sticky rules
# ---------------------------------------------------------------------------
SKEW_WHY = {
    "USDJPY": "JPY is a funding currency. In risk-off, carry trades unwind and JPY rallies sharply, so USDJPY downside (JPY calls) is bid and spot down goes with vol up.",
    "EURJPY": "JPY is a funding currency. In risk-off, carry trades unwind and JPY rallies sharply, so EURJPY downside (JPY calls) is bid and spot down goes with vol up.",
    "AUDUSD": "AUD is a high-beta, risk-sensitive currency. It sells off in risk-off, so AUD puts are bid and vol rises as spot falls.",
    "NZDUSD": "NZD is a high-beta, risk-sensitive currency. It sells off in risk-off, so NZD puts are bid and vol rises as spot falls.",
    "USDCHF": "CHF is a safe haven. In stress CHF strengthens, so USDCHF downside (CHF calls) is bid.",
    "EURCHF": "CHF is a safe haven. In stress CHF strengthens, so EURCHF downside (CHF calls) is bid.",
    "USDCAD": "CAD is a commodity and risk currency. In risk-off USD rallies against CAD, so USDCAD topside (USD calls) is bid and the RR is positive.",
    "GBPUSD": "GBP tends to weaken in risk-off and on domestic political or fiscal stress, so GBP puts carry a premium.",
    "EURUSD": "EURUSD has no strong crash direction, so its skew is small. The sign flips with which side the market fears, and lately EUR calls have carried a small premium.",
    "EURGBP": "EURGBP topside (GBP weakness) has historically been the stress scenario, so EUR calls carry a small premium.",
}


def q_skew(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    pairs = ["USDJPY", "AUDUSD", "USDCHF", "USDCAD", "EURUSD", "GBPUSD"]
    pair = str(rng.choice(pairs))
    q = static_market().quotes[pair]["1M"]
    rr = q.rr25 * 100
    correct_txt = SKEW_WHY[pair]
    distract = [SKEW_WHY[p] for p in pairs if p != pair and SKEW_WHY[p] != correct_txt]
    rng.shuffle(distract)
    opts = [correct_txt] + distract[:2] + ["Skew exists because Black-Scholes is wrong about interest rates."]
    order = rng.permutation(len(opts))
    opts = [opts[i] for i in order]
    correct = int(np.where(order == 0)[0][0])
    model = (f"**{correct_txt}**\n\n1. 1M 25d RR in {pair} is {rr:+.2f} vols (RR = call vol - put vol on {pair[:3]}).\n"
             f"2. Skew prices the direction in which the market expects big moves and rising vol. Spot-vol "
             f"correlation is the key: if spot falls when vol rises, puts are worth more than Black-Scholes says and "
             f"the RR goes negative.\n3. Compare: equity index skew is strongly negative (crash risk, leverage effect, "
             f"structural put buying). USDJPY looks like equities with the sign set by yen strength in stress.")
    return Question(section="options", subsection="1C", topic="concepts:skew", difficulty=difficulty,
                    template="skew", seed=seed,
                    prompt=f"The 1M 25-delta risk reversal in **{pair}** is **{rr:+.2f} vols**. Which explanation fits best?",
                    parts=[Part("mcq", "Explanation", opts, correct)],
                    free_text_prompt="Explain in your own words, including the spot-vol correlation.",
                    facts={"pair": pair, "rr25_1M": rr, "explanation": correct_txt}, model_answer=model,
                    rubric=["Links RR sign to spot-vol correlation", correct_txt])


def q_sticky(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    pair = str(rng.choice(["USDJPY", "AUDUSD", "USDCAD", "EURUSD", "USDCHF"]))
    mkt = fx_market(pair)
    tau = TENORS["1M"]
    pct = round(float(rng.uniform(1.0, 2.5)) * (1 if rng.random() < 0.5 else -1), 1)
    k0 = mkt.atm_strike(tau)
    v0 = mkt.vol(k0, tau)
    ms = mkt.bump_spot(pct, sticky="strike")
    k1 = ms.atm_strike(tau)
    v1 = ms.vol(k1, tau)
    md = mkt.bump_spot(pct, sticky="delta")
    v1d = md.vol(md.atm_strike(tau), tau)
    dv = (v1 - v0) * 100
    word = "Rises" if dv > 0.02 else "Falls" if dv < -0.02 else "Unchanged"
    opts = ["Rises", "Falls", "Unchanged"]
    rr = static_market().quotes[pair]["1M"].rr25 * 100
    model = (f"**Sticky strike: ATM vol {word.lower()} ({v0*100:.2f}% to {v1*100:.2f}%). Sticky delta: unchanged "
             f"({v1d*100:.2f}%).**\n\n1. Sticky strike: each strike keeps its vol. When spot moves {pct:+.1f}%, the ATM "
             f"strike moves to {k1:.{mkt.pair.decimals}f}, so ATM vol is read off the old smile at a "
             f"{'higher' if pct > 0 else 'lower'} strike. With RR {rr:+.2f} ({'calls over puts' if rr > 0 else 'puts over calls'}), "
             f"that strike's vol is {'higher' if dv > 0 else 'lower'}.\n2. Sticky delta: the smile moves with spot, so ATM "
             f"vol is unchanged and each delta keeps its vol.\n3. Why it matters: your delta depends on the rule. Under "
             f"sticky strike the 'smile delta' differs from the Black-Scholes delta by vega x d(vol)/dS.")
    return Question(section="options", subsection="1C", topic="concepts:sticky", difficulty=difficulty,
                    template="sticky", seed=seed,
                    prompt=(f"{pair} 1M: ATM {v0*100:.2f}%, 25d RR {rr:+.2f}. Spot moves {pct:+.1f}%. Under a "
                            f"**sticky-strike** smile, what happens to 1M ATM vol? And under **sticky delta**?"),
                    parts=[Part("mcq", "Sticky strike: ATM vol", opts, opts.index(word)),
                           Part("mcq", "Sticky delta: ATM vol", opts, 2)],
                    free_text_prompt="Explain the difference and when traders assume each.",
                    facts={"pair": pair, "spot_move_pct": pct, "atm_before": v0, "atm_after_sticky_strike": v1,
                           "atm_after_sticky_delta": v1d, "rr25": rr},
                    model_answer=model, rubric=["Sticky strike reads old smile at new ATM strike",
                                                "Sticky delta leaves ATM vol unchanged", "Uses the RR sign"])


# ---------------------------------------------------------------------------
# Trade expression
# ---------------------------------------------------------------------------
EVENTS = {"USDJPY": "BoJ meeting", "EURUSD": "ECB meeting", "GBPUSD": "BoE meeting", "AUDUSD": "RBA meeting",
          "USDCAD": "US payrolls", "EURJPY": "US CPI release"}
VIEWS = {
    "vol_up": ("You expect vol to rise into the event but have no view on direction.",
               "Long straddle (ATM, delta-hedged)", "Buy the event: own gamma and vega through the event day. ATM straddle "
               "maximises gamma and vega per premium and starts delta-neutral."),
    "overpriced": ("You think the market is overpricing the event: you expect a small move and a vol crush after.",
                   "Short strangle (or short straddle), delta-hedged", "Sell the event: short vega and gamma, collecting the "
                   "event premium. Strangles give room for a moderate move; know your tail risk and size for it."),
    "direction": ("You expect a large move with the base currency higher, but options look expensive.",
                  "Call spread", "Express the direction with limited premium: a call spread sells back some of the "
                  "expensive upside vol and caps the cost."),
    "skew": ("You think downside protection (the put wing) is overpriced relative to calls.",
             "Sell the risk reversal skew: buy calls, sell puts (vega-hedged)",
             "Trade the skew directly: the RR isolates put vol vs call vol. Hedge delta and residual vega so the P&L "
             "comes from the skew normalising."),
}
STRUCTS = ["Long straddle (ATM, delta-hedged)", "Short strangle (or short straddle), delta-hedged", "Call spread",
           "Sell the risk reversal skew: buy calls, sell puts (vega-hedged)", "Long calendar spread"]


def q_trade(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    pair = str(rng.choice(list(EVENTS)))
    mkt = fx_market(pair)
    event = EVENTS[pair]
    days = int(rng.choice([3, 5, 9, 12, 20]))
    views = ["vol_up", "overpriced"] + (["direction"] if difficulty >= 2 else []) + (["skew"] if difficulty == 3 else [])
    view = str(rng.choice(views))
    vtxt, struct_ans, why = VIEWS[view]
    expiries = [("1W", 7), ("2W", 14), ("1M", 30), ("3M", 91)]
    covering = [t for t, d in expiries if d > days]
    best = covering[0]
    exp_opts = [t for t, _ in expiries]
    tau = TENORS[best]
    s = build("straddle", mkt, best, 1e6)
    prem = s.value(mkt) / 1e6
    be = prem / mkt.spot * 100
    parts = [Part("mcq", "Structure", STRUCTS, STRUCTS.index(struct_ans))]
    if view in ("vol_up", "overpriced"):
        parts.append(Part("mcq", "Expiry", exp_opts, exp_opts.index(best)))
    model = (f"**{struct_ans}; expiry {best}.**\n\n1. {why}\n"
             f"2. Expiry: the {event} is in {days} days. Choose the shortest expiry that covers it ({best}). The event "
             f"day's variance is a bigger share of a short option's total variance, so short-dated options give the "
             f"most exposure to the event per premium (and you are not paying for many dull days after it).\n"
             f"3. Engine context: the {best} ATM straddle costs {prem/mkt.pair.pip:,.0f} pips ({be:.2f}% of spot); "
             f"spot needs to move about that much by expiry to break even unhedged.\n"
             f"4. Risk: after the event implied vol usually drops (crush), so a long holder should plan the exit; a "
             f"short seller is exposed to a gap move.")
    return Question(section="options", subsection="1C", topic="concepts:trade_expression", difficulty=difficulty,
                    template=f"trade_{view}", seed=seed,
                    prompt=f"**{pair}**: the {event} is in **{days} days**. {vtxt} What trade do you put on, and which expiry?",
                    parts=parts, free_text_prompt="Justify the structure and expiry, and say what could go wrong.",
                    facts={"pair": pair, "event": event, "days_to_event": days, "best_expiry": best,
                           "straddle_premium_pct": be, "view": vtxt},
                    model_answer=model,
                    rubric=[f"Structure: {struct_ans}", f"Expiry {best}: shortest covering the event",
                            "Mentions event vol crush / exit plan", "Mentions the main risk"])


TEMPLATES = {1: [q_arbitrage, q_breakeven, q_straddle_puzzle, q_trade, q_skew],
             2: [q_arbitrage, q_breakeven, q_realised_vs_implied, q_straddle_puzzle, q_skew, q_sticky, q_trade],
             3: [q_arbitrage, q_realised_vs_implied, q_sticky, q_trade, q_skew, q_straddle_puzzle]}


def generate(seed: int, difficulty: int) -> Question:
    rng = np.random.default_rng(seed)
    fn = TEMPLATES[difficulty][int(rng.integers(len(TEMPLATES[difficulty])))]
    return fn(rng, difficulty, seed)

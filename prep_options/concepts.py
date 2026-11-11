"""Section 1C: no-arbitrage, implied vs realised, gamma/theta, skew, sticky
strike vs sticky delta, and trade expression. Numbers from the engine."""
from __future__ import annotations

import numpy as np

from engine.fx_pricer import price
from engine.structures import build
from grading.question import Part, Question, chart_bar
from prep_options import calcs
from prep_options.common import fmt_num, fx_market, pick_pair, static_market


# ---------------------------------------------------------------------------
# No-arbitrage
# ---------------------------------------------------------------------------
def q_arbitrage(rng: np.random.Generator, difficulty: int, seed: int) -> Question:
    # Level 1 intuition version: what do you do? (the sized version with Givens is calcs.q_arb_calc)
    variants = ["call_spread", "call_spread", "put_spread", "butterfly", "calendar"]
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
    return Question(section="options", subsection="1C", topic="concepts:arbitrage", difficulty=difficulty,
                    template=f"arb_{v}", seed=seed, prompt=prompt,
                    parts=[Part("mcq", "Trade", opts, correct)],
                    free_text_prompt="Explain the arbitrage and the bound being violated.",
                    facts=facts, model_answer=model,
                    rubric=["Identifies the violated bound", "Correct direction of trade"])


# ---------------------------------------------------------------------------
# Gamma / theta, implied vs realised
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Level 1: which structure for which view
# ---------------------------------------------------------------------------
VIEW_MATCH = [
    ("You expect a big move or a vol rise but have no view on direction.", "Long ATM straddle",
     "It is delta-neutral at inception and maximises gamma and vega per premium. Risk: theta every day the move does not come."),
    ("You think spot will pin close to today's level at expiry and realised vol will be low.", "Long butterfly centred at today's spot",
     "The fly pays most if spot finishes at the body strike, costs little, and has capped risk. It is short gamma and short vega near the body."),
    ("You think puts will get more expensive relative to calls (skew steepens towards puts).", "Long put / short call risk reversal, delta- and vega-hedged",
     "Owning the put wing and selling the call wing isolates the skew. Hedge delta and residual vega so the P&L comes from the RR moving."),
    ("You think front-end vol will rise relative to back-end vol (term structure inverts).", "Long the near expiry, short the far expiry (short calendar), vega-weighted",
     "Being long short-dated vega and short long-dated vega profits from the front rising more. Weight by vega (or vega x sqrt(T) scaling) so a parallel move is roughly neutral."),
    ("You expect a quiet, range-bound market and implied vol to drift lower.", "Short 25-delta strangle, delta-hedged",
     "You collect theta and are short vega. Strangles leave room for moderate moves; the risk is a gap through a strike, so size for the tail."),
    ("You want upside exposure cheaply and are happy to cap the gain.", "Call spread",
     "Buying the near strike and selling the further strike cuts the premium (you sell back some of the upside vol). Delta-positive with capped payoff."),
    ("You expect a large move but straddles look expensive; you accept needing a bigger move.", "Long 25-delta strangle",
     "Cheaper than a straddle because both strikes are out of the money, but spot must travel further before it pays."),
]


def q_view_match(rng, difficulty, seed):
    i = int(rng.integers(len(VIEW_MATCH)))
    view, ans, why = VIEW_MATCH[i]
    others = [v[1] for j, v in enumerate(VIEW_MATCH) if j != i]
    rng.shuffle(others)
    opts = [ans] + others[:3]
    order = rng.permutation(4)
    opts = [opts[k] for k in order]
    correct = int(np.where(order == 0)[0][0])
    pair = pick_pair(rng)
    return Question("options", "1C", "concepts:trade_expression", difficulty, "view_match", seed,
                    prompt=f"**{pair}.** {view} Which structure expresses the view best?",
                    parts=[Part("mcq", "Structure", opts, correct)],
                    free_text_prompt="Why this structure, and what is its main risk?",
                    facts={"view": view, "answer": ans}, model_answer=f"**{ans}.**\n\n{why}",
                    rubric=[ans, why])


# ---------------------------------------------------------------------------
# Level 2: explain P&L outcomes with the Greeks (engine attribution)
# ---------------------------------------------------------------------------
PUZZLES = {
    "straddle_no_move_won": ("long", "straddle", "1M", "Spot is exactly where it was a day later, yet you made money. Why?",
                             "Implied vol rose: the vega gain beat a day of theta"),
    "straddle_moved_lost": ("long", "straddle", "1M", "A day later spot has moved {pct}%, yet you lost money. Why?",
                            "Implied vol fell: the vega loss (plus theta) beat the gamma gain"),
    "short_strangle_inside_lost": ("short", "strangle", "1M", "Spot stayed well inside both strikes, yet the short strangle lost money. Why?",
                                   "Implied vol rose: you are short vega, and the vol move cost more than the theta earned"),
    "calendar_lost_long_vega": ("long", "calendar", "1W", "You are long vega through the calendar, yet you lost money over two days. Why?",
                                "Spot moved: the short near-dated option's gamma dominated (a calendar is short gamma)"),
    "fly_pinned_lost": ("long", "butterfly", "1M", "Spot sat right on the body strike for a day, yet the long butterfly lost money. Why?",
                        "Implied vol rose: a long fly is short vega near the body, which outweighed a day of theta"),
    "call_rally_lost": ("long", "call", "1M", "Spot rallied {pct}% the day after an event, yet your long call lost money. Why?",
                        "Event vol was crushed: the vega loss beat the delta gain"),
}
DISTRACT = ["Theta is positive for this position", "Delta was hedged, so P&L must be zero",
            "Interest rates moved against you", "Gamma is negative for a long option"]


def q_puzzle(rng, difficulty, seed):
    from engine.pnl_attribution import revaluation_breakdown
    from engine.structures import build
    key = str(rng.choice(list(PUZZLES)))
    side, kind, tenor, text, ans = PUZZLES[key]
    pair = pick_pair(rng)
    mkt = fx_market(pair)
    sgn = 1 if side == "long" else -1
    s = build(kind, mkt, tenor, 1e7, side=sgn, moneyness_delta=0.25 if kind == "call" else None)
    for scale in (1.0, 1.5, 2.0, 3.0):
        pct = round(0.8 * scale, 1)
        if key == "straddle_no_move_won":
            m1 = mkt.pass_time(1).bump_vol(1.0 * scale)
        elif key == "straddle_moved_lost":
            m1 = mkt.pass_time(1).bump_spot(0.8).bump_vol(-1.5 * scale)
            pct = 0.8
        elif key == "short_strangle_inside_lost":
            m1 = mkt.pass_time(1).bump_spot(0.2).bump_vol(1.0 * scale)
        elif key == "calendar_lost_long_vega":
            m1 = mkt.pass_time(2).bump_spot(1.0 * scale)
        elif key == "fly_pinned_lost":
            m1 = mkt.pass_time(1).bump_vol(1.0 * scale)
        else:
            m1 = mkt.pass_time(1).bump_spot(0.6).bump_vol(-2.0 * scale)
            pct = 0.6
        bd = revaluation_breakdown(s.legs, mkt, m1)
        want_win = key == "straddle_no_move_won"
        if (bd["total"] > 0) == want_win:
            break
    total = bd.pop("total")
    if (total > 0) != (key == "straddle_no_move_won"):
        raise ValueError("puzzle story does not hold for these conditions")
    main = max(bd, key=lambda k: abs(bd[k]))
    opts = [ans] + list(rng.choice(DISTRACT, 3, replace=False))
    order = rng.permutation(4)
    opts = [opts[k] for k in order]
    correct = int(np.where(order == 0)[0][0])
    nice = {"delta": "delta", "gamma": "gamma (and higher-order spot)", "vega": "vega/vol", "theta": "theta"}
    model = (f"**{ans}.**\n\n1. Engine P&L: {fmt_num(total)} {mkt.pair.quote}. Breakdown (spot, then vol, then "
             f"time): " + ", ".join(f"{nice[k]} {fmt_num(v)}" for k, v in bd.items()) +
             f". Biggest driver: {nice[main]}.\n2. Lesson: an option position is a bet on realised AND implied vol, "
             f"and on time; one leg of the Greek P&L can swamp the one you were focused on.")
    return Question("options", "1C", "concepts:pnl_explain", difficulty, f"puzzle_{key}", seed,
                    prompt=f"**{pair}**: you are {side} a {tenor} {kind.replace('_', ' ')}"
                           f"{' (25-delta)' if kind == 'call' else ''}. " + text.format(pct=pct),
                    parts=[Part("mcq", "Main reason", opts, correct)],
                    free_text_prompt="Explain using the Greeks.",
                    facts={"pnl": total, "breakdown": bd, "puzzle": key}, model_answer=model,
                    rubric=[ans, f"Largest P&L term: {nice[main]}"],
                    charts=[chart_bar("P&L breakdown", list(bd.keys()), list(bd.values()), mkt.pair.quote)])


# ---------------------------------------------------------------------------
# Level 3: skew dynamics with numbers
# ---------------------------------------------------------------------------
def q_skew_pnl(rng, difficulty, seed):
    from engine.structures import build
    from grading.question import attach_givens
    pair = str(rng.choice(["USDJPY", "AUDUSD", "USDCHF"]))
    mkt = fx_market(pair)
    s = build("risk_reversal", mkt, "1M", 2.5e7, side=int(rng.choice([1, -1])))
    side = "long" if s.legs[0].notional > 0 else "short"
    from engine.fx_pricer import greeks
    vc = s.legs[0].notional * greeks(mkt.spot, s.legs[0].K, 1 / 12, mkt.rd, mkt.rf, mkt.vol(s.legs[0].K, 1 / 12), "C").vega * 0.01
    vp = s.legs[1].notional * greeks(mkt.spot, s.legs[1].K, 1 / 12, mkt.rd, mkt.rf, mkt.vol(s.legs[1].K, 1 / 12), "P").vega * 0.01
    d_atm = round(float(rng.uniform(0.5, 2.0)), 1)
    d_rr = -round(float(rng.uniform(0.3, 1.0)), 1)
    givens = {"vega_call_leg": round(vc, 0), "vega_put_leg": round(vp, 0), "d_atm": d_atm, "d_rr25": d_rr}
    labels = {"vega_call_leg": f"Vega of your 25d call leg ({mkt.pair.quote}/vol pt, signed)",
              "vega_put_leg": f"Vega of your 25d put leg ({mkt.pair.quote}/vol pt, signed)",
              "d_atm": "Change in 1M ATM vol (pts)", "d_rr25": "Change in 1M 25d RR (vols)"}

    def solver(g):
        d_call = g["d_atm"] + g["d_rr25"] / 2
        d_put = g["d_atm"] - g["d_rr25"] / 2
        return [g["vega_call_leg"] * d_call + g["vega_put_leg"] * d_put]

    q = Question("options", "1C", "concepts:skew", difficulty, "skew_pnl", seed,
                 prompt=(f"**{pair}** risk-off: 1M ATM vol rises {d_atm} and the 25d RR moves {d_rr:+} (towards puts). "
                         f"You are {side} a 1M 25d risk reversal (call over put). Assume the 25d fly is unchanged. "
                         f"Estimate your vol P&L. Does the skew move help or hurt you?"),
                 parts=[Part("numeric", f"Vol P&L ({mkt.pair.quote})", tol_rel=0.03, tol_abs=1),
                        Part("mcq", "The skew move alone", ["Helps you", "Hurts you"], 0)],
                 free_text_prompt="Explain the skew dynamics (why RRs move this way when spot falls).",
                 rubric=["Wing vol = ATM + BF +/- RR/2", "Long RR loses when RR moves towards puts",
                         "Spot-vol correlation drives skew moves"])
    attach_givens(q, givens, labels, solver)
    skew_only = givens["vega_call_leg"] * d_rr / 2 - givens["vega_put_leg"] * d_rr / 2
    q.parts[1].correct = 0 if skew_only > 0 else 1
    est = q.parts[0].correct
    q.model_answer = (f"**About {fmt_num(est)} {mkt.pair.quote}; the skew move {'helps' if skew_only > 0 else 'hurts'} you "
                      f"({fmt_num(skew_only)}).**\n\n1. With the fly fixed, 25d call vol moves dATM + dRR/2 = "
                      f"{d_atm + d_rr/2:+.2f} and 25d put vol moves dATM - dRR/2 = {d_atm - d_rr/2:+.2f}.\n"
                      f"2. P&L = vega_call x dvol_call + vega_put x dvol_put = {est:,.0f}.\n"
                      f"3. Why skews move: in {pair} the base currency falls in risk-off and vol rises with it, so "
                      f"downside (puts) reprices most: RRs move towards puts as spot falls (negative spot-vol correlation).")
    q.facts = dict(givens)
    return q


# Levels: L1 views/structures, event expiry, basic no-arbitrage, why skew exists
#         L2 explain P&L outcomes with Greeks
#         L3 sticky strike/delta with numbers, breakevens, delta-hedged P&L, skew dynamics, arbitrage with numbers
def _l3(fn):
    return lambda rng, d, seed: fn(rng, d, seed, "1C")


TEMPLATES = {1: [q_view_match, q_view_match, q_trade, q_arbitrage, q_skew],
             2: [q_puzzle],
             3: [_l3(calcs.q_sticky_calc), _l3(calcs.q_breakeven), _l3(calcs.q_rv_iv), _l3(calcs.q_arb_calc), q_skew_pnl]}


def generate(seed: int, difficulty: int) -> Question:
    for k in range(6):
        rng = np.random.default_rng(seed + k)
        fn = TEMPLATES[difficulty][int(rng.integers(len(TEMPLATES[difficulty])))]
        try:
            return fn(rng, difficulty, seed + k)
        except ValueError:
            continue
    raise RuntimeError("could not generate a consistent question")

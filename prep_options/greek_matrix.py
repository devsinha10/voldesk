"""Section 1A coverage matrices.

Level 1: first-order Greeks (delta, gamma, theta, vega, rho)
Level 2: second-order Greeks (vanna, volga, charm, speed, veta)

Each matrix = Greek x driver (spot, time, vol) x direction (up/down) x call/put
x moneyness (ITM/ATM/OTM) x long/short. A question states every condition
(pair, moneyness by delta, tenor, shock size) and is only used if the engine
gives the SAME clear direction for a small and a large version of the shock;
otherwise other conditions are tried, and cells that never resolve are reported
as unproducible.

Pairs are restricted to unadjusted-delta pairs so 'delta' has one meaning.
"""
from __future__ import annotations

import itertools
from dataclasses import replace
from typing import Optional

import numpy as np

from engine.fx_conventions import TENORS
from engine.structures import SingleMarket, Structure, build
from grading.question import Part, Question, chart_line
from prep_options.common import fx_market, spot_grid, tenor_text

L1_GREEKS = ["delta", "gamma", "theta", "vega", "rho"]
L2_GREEKS = ["vanna", "volga", "charm", "speed", "veta"]
DRIVERS = ["spot", "time", "vol"]
DIRS = ["up", "down"]
CPS = ["C", "P"]
MONEYS = ["ITM", "ATM", "OTM"]
SIDES = ["long", "short"]
PAIRS_1A = ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD"]
TENORS_1A = ["1W", "1M", "3M", "6M", "1Y"]
MONEY_DELTAS = {"ITM": [0.75, 0.85], "ATM": [None], "OTM": [0.25, 0.15, 0.10]}

LABEL = {"delta": "delta", "gamma": "gamma", "theta": "theta", "vega": "vega", "rho": "rho",
         "vanna": "vanna", "volga": "volga", "charm": "charm", "speed": "speed", "veta": "veta"}
UNITS = {"delta": "base-ccy notional", "gamma": "change in delta per 1% spot", "theta": "P&L per day",
         "vega": "P&L per vol point", "rho": "P&L per +1bp in the quote-ccy rate",
         "vanna": "change in delta per vol point", "volga": "change in vega per vol point",
         "charm": "change in delta per day", "speed": "change in gamma per 1% spot",
         "veta": "change in vega per day"}

MECH = {
    ("delta", "spot"): "Delta changes by about gamma x dS, and long-option gamma is positive: a rally raises a call's delta towards 1 and moves a put's delta towards 0; a selloff does the opposite.",
    ("delta", "vol"): "Higher vol makes every strike look closer to the money, so deltas are pulled towards 50: OTM deltas grow and ITM deltas shrink (that is vanna). Lower vol pushes them apart.",
    ("delta", "time"): "With less time left there is less chance of crossing the strike: OTM deltas decay towards 0 and ITM deltas grow towards 100 (charm). More time does the reverse.",
    ("gamma", "spot"): "Gamma peaks near the strike: spot moving towards the strike raises it, moving away lowers it.",
    ("gamma", "vol"): "Gamma lives within about one standard deviation of the strike. Higher vol spreads it out: gamma near the strike falls (ATM gamma ~ 1/(vol sqrt T)), gamma at far strikes rises.",
    ("gamma", "time"): "Near the strike, gamma grows as expiry approaches (~1/sqrt T); away from the strike it collapses because the strike becomes too many standard deviations away.",
    ("theta", "spot"): "Theta mirrors gamma (theta ~ -0.5 gamma S^2 vol^2 plus rate terms): it is largest near the strike.",
    ("theta", "vol"): "Time value scales with vol, so theta decay scales roughly with vol near the money; far from the strike higher vol also adds time value to lose.",
    ("theta", "time"): "Near the strike, decay accelerates into expiry (~1/sqrt T); far from the strike there is little time value left, so decay fades. Deep ITM options can even have positive theta from carry.",
    ("vega", "spot"): "Vega peaks near the strike, so it rises as spot moves towards the strike and falls as it moves away.",
    ("vega", "vol"): "Near the money vega is almost linear in vol (volga ~ 0); in the wings higher vol makes the strike 'closer', so vega rises (positive volga).",
    ("vega", "time"): "Vega scales with sqrt(T) near the money: less time, less vega; wing vega falls faster still.",
    ("rho", "spot"): "Rho to the quote-ccy rate is K T e^(-rd T) N(d2) for a call and -K T e^(-rd T) N(-d2) for a put: it grows as the option moves into the money (the strike payment becomes likely).",
    ("rho", "vol"): "Vol pushes N(d2) towards 1/2: an OTM option's rho grows, an ITM option's rho shrinks.",
    ("rho", "time"): "Rho is proportional to T (the strike is discounted over T), so it shrinks as time passes; ITM rho also depends on how likely exercise stays.",
    ("vanna", "spot"): "Vanna = -e^(-rf T) n(d1) d2 / vol: positive for strikes above the forward, negative below, near zero around the money, largest in size near the 25-delta points. Moving spot moves where the strike sits on that S-shaped curve.",
    ("vanna", "vol"): "Higher vol stretches the vanna profile out: the strike looks closer to the money in standard deviations, which moves its vanna along the S-shaped curve.",
    ("vanna", "time"): "As expiry approaches the vanna profile gets narrower and taller; far strikes lose vanna, nearer ones can gain.",
    ("volga", "spot"): "Volga = vega x d1 d2 / vol: ~0 at the money and positive in the wings (it peaks around the 10-15 delta points). Moving spot changes how far into the wings the strike sits.",
    ("volga", "vol"): "Higher vol brings wing strikes closer in standard deviations, so their volga (convexity in vol) changes; near the money volga stays small.",
    ("volga", "time"): "With less time the same strike is more standard deviations away; volga follows vega down overall but shifts along the wings.",
    ("charm", "spot"): "Charm (delta decay per day) is biggest for options near the 25-delta points and changes sign across the money.",
    ("charm", "vol"): "Higher vol slows the daily drift of delta because the strike looks closer in standard deviations.",
    ("charm", "time"): "Charm grows sharply into expiry: deltas snap towards 0 or 1 in the last days.",
    ("speed", "spot"): "Speed = d(gamma)/dS: positive below the strike (gamma rising towards it), negative above. Moving spot shifts where you sit on the gamma hump.",
    ("speed", "vol"): "Higher vol flattens the gamma hump, so speed (its slope) shrinks in size near the strike.",
    ("speed", "time"): "Near expiry the gamma hump becomes narrow and steep, so speed grows in size near the strike.",
    ("veta", "spot"): "Veta = d(vega)/dt. Vega bleeds fastest near the strike, so veta is most negative there.",
    ("veta", "vol"): "Higher vol changes how fast vega bleeds: wing vega bleeds differently once the strike is closer in standard deviations.",
    ("veta", "time"): "Vega decays like sqrt(T), so the bleed per day accelerates as expiry approaches.",
}


def all_cells(level: int) -> list[str]:
    greeks = L1_GREEKS if level == 1 else L2_GREEKS
    return ["|".join(c) for c in itertools.product(greeks, DRIVERS, DIRS, CPS, MONEYS, SIDES)]


def matrix_name(level: int) -> str:
    return f"1A-L{level}"


# ---------------------------------------------------------------------------
# Greek values (per position, desk units)
# ---------------------------------------------------------------------------
def greek_value(s: Structure, m: SingleMarket, g: str) -> float:
    if g in ("speed", "veta"):
        if g == "speed":
            up, dn = m.bump_spot(0.1), m.bump_spot(-0.1)
            return (s.exposure(up).gamma_1pct - s.exposure(dn).gamma_1pct) / 0.2
        return s.exposure(m.pass_time(1)).vega - s.exposure(m).vega
    e = s.exposure(m)
    return {"delta": e.delta, "gamma": e.gamma_1pct, "theta": e.theta, "vega": e.vega, "rho": e.rho_d,
            "vanna": e.vanna, "volga": e.volga, "charm": e.charm}[g]


def _with_expiry(s: Structure, mult: float, t0: float) -> Structure:
    legs = tuple(replace(l, expiry=t0 + (l.expiry - t0) * mult) for l in s.legs)
    return Structure(s.name, legs)


def _shocked(s: Structure, m: SingleMarket, driver: str, direction: str, size: float):
    """(structure, market) after the shock. size: % spot, vol pts, or time fraction/multiplier."""
    if driver == "spot":
        return s, m.bump_spot(size if direction == "up" else -size)
    if driver == "vol":
        return s, m.bump_vol(size if direction == "up" else -size)
    tau = s.legs[0].expiry - m.t
    if direction == "down":   # time passes
        return s, m.pass_time(tau * 365 * size)
    return _with_expiry(s, size, m.t), m   # longer expiry, same strike


def _shock_text(driver: str, direction: str, size: float, tenor: str, tau: float, vol: float) -> str:
    if driver == "spot":
        return f"spot {'rallies' if direction == 'up' else 'sells off'} {size:.1f}% (sticky strike)"
    if driver == "vol":
        return f"implied vol {'rises' if direction == 'up' else 'falls'} {size:.1f} vol points (from {vol*100:.1f}%), all strikes"
    if direction == "down":
        return f"{tau * 365 * size:.0f} days pass (spot and vol unchanged)"
    return (f"compare it with the same strike at a {tau * size * 12:.0f}-month expiry instead of {tenor} "
            f"(longer time to expiry, spot and vol unchanged)") if tau * size >= 1 / 12 else \
        f"compare it with the same strike at a {tau * size * 365:.0f}-day expiry instead of {tenor} (longer time to expiry)"


def _sizes(driver: str, direction: str, vol: float) -> list[float]:
    if driver == "spot":
        return [1.0, 1.5, 2.0, 3.0]
    if driver == "vol":
        cap = 0.6 * vol * 100
        return [x for x in (2.0, 3.0, 4.0) if direction == "up" or x <= cap] or [round(cap, 1)]
    return [0.5, 0.75] if direction == "down" else [2.0, 3.0]


def _small(driver: str, direction: str, size: float) -> float:
    if driver == "time":
        return size / 3 if direction == "down" else 1 + (size - 1) / 3
    return size / 3


def evaluate(cell: str, pair: str, tenor: str, mdelta: Optional[float], size: float,
             allow_flat: bool = True) -> Optional[dict]:
    """Engine check for one set of conditions. Returns details if the direction is clear."""
    g, driver, direction, cp, money, side = cell.split("|")
    m = fx_market(pair)
    sgn = 1 if side == "long" else -1
    s = build("call" if cp == "C" else "put", m, tenor, 1e7 * sgn, moneyness_delta=mdelta)
    b = greek_value(s, m, g)
    s1, m1 = _shocked(s, m, driver, direction, size)
    a = greek_value(s1, m1, g)
    s2, m2 = _shocked(s, m, driver, direction, _small(driver, direction, size))
    a_small = greek_value(s2, m2, g)
    ref = abs(greek_value(build("call", m, tenor, 1e7, moneyness_delta=0.25), m, g)) or 1.0
    first_order = g in L1_GREEKS
    base = dict(before=b, after=a, after_small=a_small, ref=ref, struct=s, mkt=m, shocked=(s1, m1))
    # robustly flat: tiny change for BOTH shock sizes -> a clear 'roughly unchanged'
    flat_scale = abs(b) if first_order else max(abs(b), ref)
    if first_order and np.sign(a) != np.sign(b):
        flat_scale = 0
    if allow_flat and flat_scale > 0 and abs(b) >= (0.05 * ref if first_order else 0) and \
            abs(a - b) < 0.015 * flat_scale and abs(a_small - b) < 0.015 * flat_scale:
        return {**base, "change": a - b, "up": None}
    if first_order:
        # size-based: no sign flips, measurable before value, clear and consistent change in size
        if b == 0 or np.sign(a) != np.sign(b) or np.sign(a_small) != np.sign(b) or abs(b) < 0.05 * ref:
            return None
        d_big, d_small = abs(a) - abs(b), abs(a_small) - abs(b)
        scale = abs(b)
        thr = 0.01 * 1e7 if g == "delta" else 0.03 * scale
    else:
        d_big, d_small = a - b, a_small - b
        scale = max(abs(a), abs(b), 0.05 * ref)
        thr = 0.03 * scale
        if abs(d_big) < 0.02 * ref:
            return None
    if np.sign(d_big) != np.sign(d_small) or abs(d_big) < thr or abs(d_small) < 0.3 * thr:
        return None
    return {**base, "change": d_big, "up": bool(d_big > 0)}


def find_conditions(cell: str, rng: np.random.Generator, tries: int = 40) -> Optional[dict]:
    g, driver, direction, cp, money, side = cell.split("|")
    combos = [(p, t, md) for p in PAIRS_1A for t in TENORS_1A for md in MONEY_DELTAS[money]]
    order = rng.permutation(len(combos))
    for allow_flat in (False, True):   # prefer a clear direction; 'unchanged' only if nothing else resolves
        for k in order[:tries]:
            pair, tenor, md = combos[int(k)]
            if driver == "time" and direction == "up" and tenor == "1Y":
                continue
            vol = fx_market(pair).vol(fx_market(pair).forward(TENORS[tenor]), TENORS[tenor])
            for size in _sizes(driver, direction, vol):
                r = evaluate(cell, pair, tenor, md, size, allow_flat)
                if r:
                    r.update(pair=pair, tenor=tenor, mdelta=md, size=size, vol=vol)
                    return r
    return None


_UNPRODUCIBLE: set = set()


def _money_text(money: str, md: Optional[float], cp: str) -> str:
    kind = "call" if cp == "C" else "put"
    if money == "ATM":
        return f"ATM {kind}"
    lbl = f"{int(round(md * 100))}-delta"
    if money == "ITM":
        return f"{'deep ITM ' if md >= 0.85 else 'ITM '}{lbl} {kind}"
    return f"{lbl} OTM {kind}"


def matrix_question(seed: int, level: int, covered: Optional[set] = None) -> Question:
    rng = np.random.default_rng(seed)
    cells = [c for c in all_cells(level) if c not in _UNPRODUCIBLE]
    todo = [c for c in cells if not covered or c not in covered] or cells
    order = rng.permutation(len(todo))
    res, cell = None, None
    for k in order[:25]:
        cell = todo[int(k)]
        res = find_conditions(cell, rng)
        if res:
            break
        _UNPRODUCIBLE.add(cell)
    if res is None:
        raise RuntimeError("no producible cell found")
    return _build_question(cell, res, level, seed, rng)


def _contrast(cell: str, res: dict, rng) -> str:
    g, driver, direction, cp, money, side = cell.split("|")
    others = [m for m in MONEYS if m != money]
    for m2 in others:
        c2 = "|".join([g, driver, direction, cp, m2, side])
        for md in MONEY_DELTAS[m2]:
            r2 = evaluate(c2, res["pair"], res["tenor"], md, res["size"])
            if r2:
                same = r2["up"] == res["up"]
                word = _dir_word(g, r2["up"], side)
                mt = _money_text(m2, md, cp)
                art = "an" if mt[0] in "AEIOU" else "a"
                return (f"Contrast: for {art} {mt} with the same tenor and shock, the engine says "
                        f"{LABEL[g]} {word}" + (" too." if same else ", the opposite way. Where the strike sits matters."))
    return ""


def _dir_word(g: str, up, side: str) -> str:
    if up is None:
        return "stays roughly unchanged"
    if g in L1_GREEKS:
        return "grows in size" if up else "shrinks in size"
    return "rises" if up else "falls"


def _build_question(cell: str, res: dict, level: int, seed: int, rng) -> Question:
    g, driver, direction, cp, money, side = cell.split("|")
    pair, tenor, md, size = res["pair"], res["tenor"], res["mdelta"], res["size"]
    s, m = res["struct"], res["mkt"]
    leg = s.legs[0]
    tau = TENORS[tenor]
    pip_dec = 5
    opt = _money_text(money, md, cp)
    shock = _shock_text(driver, direction, size, tenor, tau, res["vol"])
    first = g in L1_GREEKS
    if first:
        opts = ["Grows in size", "Shrinks in size", "Roughly unchanged"]
        q_dir = f"What happens to the **size** of your {LABEL[g]} exposure?"
    else:
        opts = ["Rises (more positive)", "Falls (more negative)", "Roughly unchanged"]
        q_dir = f"What happens to your **{LABEL[g]}** exposure (signed)?"
    correct_dir = 2 if res["up"] is None else (0 if res["up"] else 1)
    b = res["before"]
    sign_opts = ["Positive (long)", "Negative (short)", "Roughly zero"]
    sign_idx = 2 if abs(b) < 0.1 * res["ref"] else (0 if b > 0 else 1)
    prompt = (f"You are **{side} a {tenor_text(tenor)} {pair} {opt}** (notional {pair[:3]} 10m, strike "
              f"{leg.K:.{pip_dec}f}, spot {m.spot:.{pip_dec}f}, spot delta unadjusted).\n\n"
              f"**Change:** {shock}.\n\n{q_dir}")
    parts = [Part("mcq", f"Sign of your {LABEL[g]} now", sign_opts, sign_idx, weight=0.5),
             Part("mcq", f"Change in your {LABEL[g]}", opts, correct_dir)]
    mech = MECH.get((g, driver), "")
    if driver == "time" and direction == "up":
        mech = "(Here the option has MORE time to expiry, so read this in reverse.) " + mech
    contrast = _contrast(cell, res, rng)
    word = _dir_word(g, res["up"], side)
    model = (f"**Answer: your {LABEL[g]} {word}** ({sign_opts[sign_idx].split(' ')[0].lower()} to start).\n\n"
             f"1. Sign: you are {side} the option, so your {LABEL[g]} has {'the same sign as' if side == 'long' else 'the opposite sign to'} "
             f"a long {('call' if cp == 'C' else 'put')}'s.\n"
             f"2. Intuition: {mech}\n"
             f"3. Engine: {LABEL[g]} goes from {b:,.0f} to {res['after']:,.0f} ({UNITS[g]}). A shock one third the "
             f"size gives {res['after_small']:,.0f}, "
             + ("also under 1.5% different, so the change is too small to matter for any shock size here.\n"
                if res["up"] is None else "the same direction, so the answer does not depend on the shock size.\n")
             + (f"4. {contrast}\n" if contrast else ""))
    spots = spot_grid(m, tau)
    series = {"Before": [greek_value(s, m.bump_spot((x / m.spot - 1) * 100), g) for x in spots]}
    if driver != "spot":
        s1, m1 = res["shocked"]
        series["After"] = [greek_value(s1, m1.bump_spot((x / m1.spot - 1) * 100), g) for x in spots]
    charts = [chart_line(f"{LABEL[g].capitalize()} vs spot", spots, series, "Spot", UNITS[g],
                         vline=res["shocked"][1].spot, vline_label="spot after")]
    return Question(section="options", subsection="1A", topic=f"greeks:{g}", difficulty=level,
                    template=f"matrix_L{level}", seed=seed, prompt=prompt, parts=parts,
                    free_text_prompt="Why? (one or two sentences)",
                    facts={"cell": cell, "pair": pair, "tenor": tenor, "option": opt, "side": side, "shock": shock,
                           "greek": g, "units": UNITS[g], "before": b, "after": res["after"],
                           "after_small_shock": res["after_small"], "direction": word},
                    model_answer=model, rubric=[f"{LABEL[g]} {word}", f"Sign now: {sign_opts[sign_idx]}", mech],
                    charts=charts, coverage_cell=(matrix_name(level), cell), tags=[g, driver, money, side])


# ---------------------------------------------------------------------------
# Level 2: first-order Greek moves explained by a named second-order Greek
# ---------------------------------------------------------------------------
VIA = [  # (first-order greek that moves, driver, second-order greek that explains it)
    ("vega", "spot", "vanna"), ("delta", "vol", "vanna"), ("vega", "vol", "volga"),
    ("delta", "time", "charm"), ("gamma", "spot", "speed"), ("vega", "time", "veta"),
]
VIA_WHY = {
    "vanna": "Vanna is both d(delta)/d(vol) and d(vega)/d(spot).",
    "volga": "Volga is d(vega)/d(vol): how vega itself responds to vol.",
    "charm": "Charm is d(delta)/d(time): how delta drifts as time passes.",
    "speed": "Speed is d(gamma)/d(spot): the slope of the gamma hump.",
    "veta": "Veta is d(vega)/d(time): how fast vega bleeds.",
}


def via_question(seed: int, level: int = 2) -> Question:
    rng = np.random.default_rng(seed)
    for _ in range(30):
        first, driver, second = VIA[int(rng.integers(len(VIA)))]
        cp = str(rng.choice(CPS))
        money = str(rng.choice(["ITM", "OTM"]))
        side = str(rng.choice(SIDES))
        direction = "down" if driver == "time" else str(rng.choice(DIRS))
        pair = str(rng.choice(PAIRS_1A))
        tenor = str(rng.choice(["1M", "3M", "6M"]))
        md = float(rng.choice(MONEY_DELTAS[money]))
        m = fx_market(pair)
        sgn = 1 if side == "long" else -1
        s = build("call" if cp == "C" else "put", m, tenor, 1e7 * sgn, moneyness_delta=md)
        sec = greek_value(s, m, second)
        size = {"spot": 0.5, "vol": 1.0, "time": 0.1}[driver]
        s1, m1 = _shocked(s, m, driver, direction, size)
        b, a = greek_value(s, m, first), greek_value(s1, m1, first)
        ref = abs(greek_value(build("call", m, tenor, 1e7, moneyness_delta=0.25), m, second)) or 1
        if abs(sec) < 0.2 * ref or abs(a - b) < 0.01 * max(abs(b), 1):
            continue
        # direction implied by the second-order Greek (time 'passes': dt>0 in charm/veta convention)
        dvar = {"spot": 1 if direction == "up" else -1, "vol": 1 if direction == "up" else -1, "time": 1}[driver]
        implied_up = np.sign(sec) * dvar > 0
        if implied_up != (a > b):
            continue  # nonlinearity would contradict the first-order reasoning: pick other conditions
        opt = _money_text(money, md, cp)
        shock = _shock_text(driver, direction, size if driver != "time" else size, tenor, TENORS[tenor],
                            m.vol(m.forward(TENORS[tenor]), TENORS[tenor]))
        opts = ["Rises (more positive)", "Falls (more negative)", "Roughly unchanged"]
        prompt = (f"You are **{side} a {tenor_text(tenor)} {pair} {opt}** (notional {pair[:3]} 10m). "
                  f"**Change:** {shock}.\n\nUsing **{second}**, does your **{first}** exposure rise or fall? "
                  f"What is the sign of your {second}?")
        sign_opts = ["Positive", "Negative"]
        model = (f"**Your {second} is {'positive' if sec > 0 else 'negative'}, so your {first} "
                 f"{'rises' if a > b else 'falls'}.**\n\n1. {VIA_WHY[second]}\n2. {MECH.get((second, 'spot'), '')}\n"
                 f"3. Change in {first} ~ {second} x change in {driver}: sign({second}) = "
                 f"{'+' if sec > 0 else '-'}, change in {driver} = {'+' if dvar > 0 else '-'}{' (time passing)' if driver == 'time' else ''}.\n"
                 f"4. Engine: {second} = {sec:,.0f} ({UNITS[second]}); {first} goes from {b:,.0f} to {a:,.0f} ({UNITS[first]}).")
        return Question(section="options", subsection="1A", topic=f"greeks:{second}", difficulty=level,
                        template="via_second_order", seed=seed, prompt=prompt,
                        parts=[Part("mcq", f"Sign of your {second}", sign_opts, 0 if sec > 0 else 1, weight=0.5),
                               Part("mcq", f"Your {first} exposure", opts, 0 if a > b else 1)],
                        free_text_prompt="Explain using the second-order Greek.",
                        facts={"first": first, "second": second, "second_value": sec, "first_before": b,
                               "first_after": a, "shock": shock, "option": opt, "side": side},
                        model_answer=model, rubric=[VIA_WHY[second], f"{first} {'rises' if a > b else 'falls'}"],
                        tags=[first, second, driver])
    raise RuntimeError("no clear via-question found")

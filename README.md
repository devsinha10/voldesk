# VolDesk

Personal training app for options, rates and FX vol interviews, plus a sell-side G10 FX options trading simulator.
Every price, Greek and model answer comes from the tested engine in `engine/`. Claude is only used to mark written
answers and to write session reviews, and it is always handed the engine's numbers.

## Run it

```bash
pip install -r requirements.txt
```

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # optional: without it you self-mark against the engine answer
```

```bash
streamlit run app.py
```

```bash
python -m pytest
```

## What is where

| Path | What |
|---|---|
| `config.yaml` | All market parameters: spots, rates, vol grids, regimes, events, limits, client mix, LLM model. Values are plausible levels, not live data: check and update them. |
| `engine/fx_pricer.py` | Garman-Kohlhagen price, Greeks (incl. vanna, volga, charm), IV solver, `Pricer` protocol and `compare_pricers` |
| `engine/fx_conventions.py` | Pairs, pips, forwards, delta conventions, DNS ATM, strike from delta |
| `engine/smile.py`, `engine/surface.py` | Quotes to pillar strikes, SABR (beta 1) per tenor with vanna-volga fallback, total-variance interpolation, arbitrage checks |
| `engine/rates.py` | Bonds, duration, convexity, DV01, curves, swaps, Bachelier swaptions, CF/CTD, carry/roll, OIS probabilities |
| `engine/structures.py` | Structures, scenario markets (spot/vol/skew/term/time bumps), desk-unit exposures |
| `engine/pnl_attribution.py` | Taylor P&L attribution (simulator) and exact revaluation breakdown (drills) |
| `engine/market_sim.py` | Simulator market: correlated currencies, stochastic vol, jumps, regimes, events, intervention |
| `prep_options/`, `prep_rates/` | Question generators with engine model answers |
| `simulator/` | Book, client flow, session (risk, limits, P&L ledger, log), debriefs |
| `grading/` | Question model, Claude marking (structured JSON, SQLite cache) |
| `progress/` | SQLite storage, Leitner boxes, mixed review |
| `views/` | Streamlit pages |

## Conventions (also shown on screen)

* Spot quoted as QUOTE per BASE. Notional in base currency. Premium in quote pips and % of base.
* Spot delta up to and including 1Y. Premium-adjusted delta for pairs whose premium is paid in the base currency:
  USDJPY, USDCHF, USDCAD and the EUR crosses (premium in EUR). Others unadjusted.
* ATM = delta-neutral straddle. RR = vol(call) minus vol(put).
* BF uses the **smile strangle** convention: vol25C = ATM + BF + RR/2, vol25P = ATM + BF - RR/2.
  Real broker quotes use the market (broker) strangle, which needs an iterative solve; it is not implemented.
* Time is ACT/365 calendar time; no holiday calendars, no spot/delivery lag. Rates are flat per currency,
  continuously compounded (override per tenor under `rate_curves`).
* SABR fits ATM exactly and the four wing quotes by least squares (3 parameters, 5 quotes), so wings match to
  within about 0.15 vol; outside that tolerance the smile falls back to vanna-volga.

## Simulator notes

* 10 real minutes = 10 days, one tick per 1.5s (config). The seed fixes the market path and the client flow, and is
  logged, so the same seed (and regime) replays the same market whatever you trade.
* Regimes (calm, trending, risk-off, CB week, intervention) set realised/implied gap, jumps, vol-of-vol, skew
  pressure and spot/vol correlation multipliers. Levels 2 and 3 can also flip a pair's spot/vol relationship
  mid-session (logged as a news item).
* Scheduled events add their variance to every expiry that covers them, then that variance is removed when the
  number prints (vol crush). ATM calendar arbitrage is enforced every tick; smiles are butterfly-checked on each full
  refit (every 5th tick) and damped if needed.
* P&L ledger is exact: total = client edge + hedging costs + carry + Greek terms + unexplained (Taylor residual).
  Limit breaches are penalised separately in the score.
* Informed clients (mostly macro funds) push the market their way after they ask for a price, whether or not you trade.

## Plug in your own pricer

Any class with `price(S, K, T, rd, rf, vol, call_put)` works. Use the Engine Lab page, or:

```python
from engine.fx_pricer import compare_pricers
df = compare_pricers(MyPricer())
```

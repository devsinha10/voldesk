"""Engine Lab: surfaces, a pricer calculator, and a harness to test your own pricer."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engine.config import reload_config
from engine.fx_conventions import PAIRS, TENOR_LIST, TENORS, get_pair, option_premium
from engine.fx_pricer import GKPricer, compare_pricers, greeks
from engine.market_data import build_market

st.title("Engine Lab")


@st.cache_resource
def market():
    return build_market()


if st.sidebar.button("Reload config.yaml"):
    reload_config()
    market.clear()
m = market()
tabs = st.tabs(["Vol surface", "Pricer", "Test your own pricer"])

with tabs[0]:
    pair = st.selectbox("Pair", list(PAIRS))
    s = m.surface(pair)
    p = get_pair(pair)
    st.caption(f"Spot {m.spots[pair]:.{p.decimals}f} ({m.source}). {p.convention_label()}")
    st.dataframe(s.quotes_table().style.format({c: "{:.2f}" for c in ["ATM", "25RR", "25BF", "10RR", "10BF"]}),
                 use_container_width=True)
    arb = s.check_arbitrage()
    st.write(f"Arbitrage check: calendar {'OK' if arb.calendar_ok else arb.calendar_violations}, "
             f"butterfly {'OK' if arb.butterfly_ok else arb.butterfly_violations}")
    fig = go.Figure()
    for t in ["1W", "1M", "3M", "1Y"]:
        sm = s.smiles[t]
        sd = sm.quotes.atm * np.sqrt(sm.T)
        Ks = sm.F * np.exp(np.linspace(-2.5 * sd, 2.5 * sd, 80))
        dl = [sm.delta_at(K, "C") for K in Ks]
        fig.add_trace(go.Scatter(x=dl, y=np.asarray(sm.vol(Ks)) * 100, mode="lines", name=t))
        fig.add_trace(go.Scatter(x=[sm.delta_at(sm.pillar_strikes[n], "C") for n in sm.pillar_vols],
                                 y=[v * 100 for v in sm.pillar_vols.values()], mode="markers",
                                 name=f"{t} quotes", showlegend=False))
    fig.update_layout(title="Smile vs call delta (lines: SABR fit; dots: market pillars)", xaxis_title="call delta",
                      yaxis_title="vol %", height=380, template="plotly_white", xaxis_autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
    rows = [{"tenor": t, "model": sm.model, **{k: round(v, 4) for k, v in sm.params.items()},
             "max fit error (vol)": round(max(abs(e) for e in sm.fit_errors.values()) * 100, 3)}
            for t, sm in s.smiles.items()]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

with tabs[1]:
    c = st.columns(4)
    pair = c[0].selectbox("Pair ", list(PAIRS), key="pr_pair")
    p = get_pair(pair)
    S = c[1].number_input("Spot", value=float(m.spots[pair]), format="%.5f")
    tenor = c[2].selectbox("Tenor", TENOR_LIST, index=5)
    cp = c[3].selectbox("Call/Put", ["C", "P"])
    T = TENORS[tenor]
    surf = m.surface(pair)
    K = st.number_input("Strike", value=float(round(surf.atm_strike(tenor), p.decimals)), format="%.5f")
    vol = st.number_input("Vol % (default from the surface)", value=float(round(surf.vol(K, T) * 100, 3)))
    rd, rf = m.rd(pair, T), m.rf(pair, T)
    g = greeks(S, K, T, rd, rf, vol / 100, cp)
    prem = option_premium(S, K, T, rd, rf, vol / 100, cp, p.pip)
    st.write(f"Forward {S * np.exp((rd - rf) * T):.{p.decimals}f}; rd ({p.quote}) {rd*100:.2f}%, rf ({p.base}) {rf*100:.2f}%")
    st.dataframe(pd.DataFrame([{"premium (pips)": prem["pips"], "premium (% base)": prem["pct_base"],
                                "spot delta": g.delta, "PA delta": g.delta_pa, "fwd delta": g.delta_fwd,
                                "gamma": g.gamma, "vega /1%": g.vega / 100, "theta /day": g.theta / 365,
                                "vanna": g.vanna, "volga": g.volga, "charm /day": g.charm / 365}]).T
                 .rename(columns={0: "per 1 unit base"}), use_container_width=True)

with tabs[2]:
    st.markdown("Paste a Python class with a `price(self, S, K, T, rd, rf, vol, call_put)` method "
                "(call_put is 'C' or 'P'). It runs locally and is compared with the reference GK pricer on a grid.")
    code = st.text_area("Your pricer", height=260, value='''import math
from statistics import NormalDist
N = NormalDist().cdf

class MyPricer:
    def price(self, S, K, T, rd, rf, vol, call_put):
        d1 = (math.log(S / K) + (rd - rf + 0.5 * vol * vol) * T) / (vol * math.sqrt(T))
        d2 = d1 - vol * math.sqrt(T)
        if call_put == "C":
            return S * math.exp(-rf * T) * N(d1) - K * math.exp(-rd * T) * N(d2)
        return K * math.exp(-rd * T) * N(-d2) - S * math.exp(-rf * T) * N(-d1)
''')
    if st.button("Compare"):
        ns: dict = {}
        try:
            exec(code, ns)  # local, user-supplied code by design
            cls = next(v for v in ns.values() if isinstance(v, type) and hasattr(v, "price"))
            df = compare_pricers(cls(), GKPricer())
            st.metric("Max abs difference (pips per unit)", f"{df['diff_pips'].abs().max():.6f}")
            st.dataframe(df.sort_values("diff", key=abs, ascending=False).head(20), hide_index=True,
                         use_container_width=True)
        except Exception as e:  # show the user's error
            st.error(f"{type(e).__name__}: {e}")

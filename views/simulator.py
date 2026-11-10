"""Section 3: FX Vol Simulator (sell-side G10 FX options desk)."""
from __future__ import annotations

import secrets
import warnings

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engine.config import load_config
from engine.fx_conventions import TENOR_LIST, get_pair
from progress import db
from simulator.clients import CLIENT_LABEL
from simulator.debrief import claude_review, rule_based_review, scorecard
from simulator.session import IDB_POINTS, SimSession

warnings.filterwarnings("ignore", category=RuntimeWarning)
CFG = load_config()["simulator"]
ss = st.session_state


def fm(x: float, d: int = 1) -> str:
    a = abs(x)
    s = "-" if x < 0 else ""
    if a >= 1e9:
        return f"{s}{a/1e9:.{d}f}bn"
    if a >= 1e6:
        return f"{s}{a/1e6:.{d}f}m"
    if a >= 1e3:
        return f"{s}{a/1e3:.{d}f}k"
    return f"{s}{a:.0f}"


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
def setup_screen() -> None:
    st.title("FX Vol Simulator")
    st.markdown("You run a **sell-side G10 FX options book**. Clients ask for prices, news hits, and you manage the risk. "
                "10 real minutes = 10 trading days.")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        level = st.radio("Intensity", [1, 2, 3], horizontal=True, format_func=lambda x: f"Level {x}")
        st.caption({1: "One pair, light flow, events announced in advance, pause button (auto-pause at each day end), wide limits.",
                    2: "Two or three pairs, steady flow, surprise headlines, normal limits, no pause.",
                    3: "Full G10 book, bursts of flow, regime shifts, intervention-style shocks, tight limits, no pause."}[level])
        seed_txt = st.text_input("Seed (blank = random; reuse a seed to replay a session)", "")
        live = st.checkbox("Live spot snapshot at start (frankfurter.app, ECB rates; falls back to config)", value=True)
        with st.expander("Practice options"):
            regime = st.selectbox("Regime", ["Random (hidden until the end)", "calm", "trending", "risk_off", "cb_week",
                                             "intervention"])
        if st.button("Start session", type="primary"):
            seed = int(seed_txt) if seed_txt.strip().isdigit() else secrets.randbelow(2**31 - 1)
            with st.spinner("Building the market..."):
                sess = SimSession(seed, level, use_live=live, regime=None if regime.startswith("Random") else regime)
            sid = db.create_session(seed, level, sess.market.regime, sess.pairs)
            db.log_events(sid, sess.new_log_entries())
            ss.sim, ss.sim_id, ss.sim_msgs, ss.sim_review = sess, sid, [], None
            st.rerun()
    with c2:
        st.markdown("**How to quote**")
        st.markdown("- Vanilla / straddle: option vol, e.g. `7.10 / 7.40`\n- Strangle: one vol for both wings\n"
                    "- Risk reversal: RR in vols (call minus put), e.g. `-1.40 / -1.10`\n"
                    "- Butterfly: fly in vols (avg wing minus ATM), e.g. `0.15 / 0.35`\n\n"
                    "Clients trade if your price beats a hidden competitive level. You see who they were only after the trade.")
        st.markdown("**Conventions**: spot delta up to 1Y, premium-adjusted for USDJPY, USDCHF, USDCAD and the EUR "
                    "crosses; ATM = delta-neutral straddle; BF = smile strangle.")


# ---------------------------------------------------------------------------
# Live dashboard
# ---------------------------------------------------------------------------
def top_bar(sess: SimSession) -> None:
    m = sess.market
    c = st.columns([1.1, 1.3, 1.1, 1.1, 1.0])
    c[0].metric("Day", f"{min(m.day + 1, m.days)} / {m.days}")
    c[1].progress(min(m.tick / m.total_ticks, 1.0), text=f"tick {m.tick}/{m.total_ticks}  seed {sess.seed}")
    c[2].metric("Total P&L (USD)", fm(sess.pnl_usd), delta=fm(sess.pnl_usd - (sess.pnl_hist[-2][1] if len(sess.pnl_hist) > 1 else 0)))
    c[3].metric("Limit penalties", fm(-sess.penalty_usd))
    with c[4]:
        if sess.lv.get("pause"):
            if st.button("▶ Resume" if sess.paused else "⏸ Pause", key="pause_btn", use_container_width=True):
                sess.toggle_pause()
        else:
            st.caption("No pause at this level")
        if sess.paused:
            st.caption("PAUSED")
    cols = st.columns(min(len(sess.pairs), 5))
    for i, p in enumerate(sess.pairs):
        pp = get_pair(p)
        S = m.spot(p)
        chg = (S / m.day_open_spot[p] - 1) * 100
        cols[i % len(cols)].metric(p, f"{S:.{pp.decimals}f}", f"{chg:+.2f}% today")


def rfq_panel(sess: SimSession) -> None:
    st.subheader("Client RFQs")
    m = sess.market
    rfqs = sess.open_rfqs()
    if not rfqs:
        st.caption("No open requests.")
    for r in rfqs[:6]:
        left = max((r.expires_tick - m.tick) * CFG["tick_seconds"], 0)
        with st.container(border=True):
            strikes = ", ".join(f"{l.cp} {l.K:.{get_pair(r.pair).decimals}f}" for l in r.legs)
            st.markdown(f"**#{r.id} {r.describe()}**  \nStrikes: {strikes}  \nQuote in: *{r.quote_unit()}*")
            st.progress(min(left / CFG["quote_timeout_s"][1], 1.0), text=f"⏱ {left:.0f}s")
            with st.form(f"q{r.id}", clear_on_submit=False, border=False):
                c1, c2, c3, c4 = st.columns([1, 1, 0.8, 0.8])
                bid = c1.number_input("Bid", value=None, step=0.05, format="%.2f", key=f"bid{r.id}")
                off = c2.number_input("Offer", value=None, step=0.05, format="%.2f", key=f"off{r.id}")
                go_q = c3.form_submit_button("Quote", type="primary")
                go_p = c4.form_submit_button("Pass")
            if go_q:
                if bid is None or off is None:
                    ss.sim_msgs.append("Enter both bid and offer.")
                else:
                    res = sess.quote(r.id, float(bid), float(off))
                    ss.sim_msgs.append(f"#{r.id}: {res['msg']}")
            if go_p:
                sess.pass_rfq(r.id)
    for msg in ss.sim_msgs[-4:][::-1]:
        st.caption(msg)


def hedge_panel(sess: SimSession) -> None:
    tabs = st.tabs(["Spot hedge", "Interdealer vol screen", "Positions"])
    with tabs[0]:
        for p in sess.pairs:
            r = sess.risk.get(p, {})
            pp = get_pair(p)
            c1, c2 = st.columns([2, 1])
            c1.markdown(f"**{p}** delta {fm(r.get('delta_base', 0))} {pp.base} "
                        f"(PA {fm(r.get('delta_pa_base', 0))}), {fm(r.get('delta_usd', 0))} USD")
            if c2.button(f"Delta-hedge {p}", key=f"dh{p}"):
                ss.sim_msgs.append(sess.delta_hedge(p)["msg"])
        with st.form("spot_form", border=False):
            c1, c2, c3 = st.columns([1, 1, 1])
            pair = c1.selectbox("Pair", sess.pairs, key="sp_pair")
            amt = c2.number_input("Amount (base, millions; + buy, - sell)", value=0.0, step=5.0, key="sp_amt")
            if c3.form_submit_button("Execute spot"):
                ss.sim_msgs.append(sess.spot_hedge(pair, amt * 1e6)["msg"])
        st.caption(f"Spot spread now: {CFG['spot_spread_pips'][sess.pairs[0]] * sess.stress_mult():.1f} pips in {sess.pairs[0]} "
                   f"(widens with stress).")
    with tabs[1]:
        pair = st.selectbox("Pair", sess.pairs, key="idb_pair")
        rows = sess.idb_screen(pair)
        df = pd.DataFrame([{**{"Tenor": r["Tenor"]}, **{pt: f"{r[pt][0]:.2f} / {r[pt][1]:.2f}" for pt in IDB_POINTS}}
                           for r in rows]).set_index("Tenor")
        st.dataframe(df, use_container_width=True)
        with st.form("idb_form", border=False):
            c = st.columns(5)
            tenor = c[0].selectbox("Tenor", TENOR_LIST, index=3, key="idb_t")
            point = c[1].selectbox("Strike", list(IDB_POINTS), index=2, key="idb_pt")
            side = c[2].selectbox("Side", ["Buy", "Sell"], key="idb_side")
            notional = c[3].number_input("Notional (m base)", value=25.0, step=5.0, key="idb_n")
            straddle = c[4].checkbox("ATM straddle", key="idb_str")
            if st.form_submit_button("Execute on IDB"):
                if straddle and point != "ATM":
                    ss.sim_msgs.append("Straddles trade at the ATM strike only.")
                else:
                    ss.sim_msgs.append(sess.idb_trade(pair, tenor, point, 1 if side == "Buy" else -1, notional * 1e6,
                                                      straddle)["msg"])
    with tabs[2]:
        blotter(sess)


def blotter(sess: SimSession) -> None:
    rows = []
    for p in sess.book.positions:
        m = sess.mkt(p.pair)
        pp = get_pair(p.pair)
        rows.append({"id": p.id, "pair": p.pair, "type": p.kind if p.kind == "spot" else f"{p.cp} option",
                     "label": p.label, "strike": round(p.K, pp.decimals),
                     "expiry (days)": round((p.expiry - m.t) * 365, 1) if p.kind == "option" else None,
                     "notional (m)": round(p.notional / 1e6, 2), "premium (pips)": round(p.premium / pp.pip, 1) if p.kind == "option" else None,
                     "value (quote ccy)": round(sess.book.position_value(p, m)), "source": p.source})
    if not rows:
        st.caption("Flat book.")
        return
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True, height=260)
    with st.form("close_form", border=False):
        c1, c2, c3 = st.columns(3)
        pid = c1.number_input("Position id", min_value=1, step=1, key="cl_id")
        new_t = c2.selectbox("Roll to", TENOR_LIST, index=4, key="cl_t")
        a, b = c3.columns(2)
        if a.form_submit_button("Close"):
            ss.sim_msgs.append(sess.close_position(int(pid))["msg"])
        if b.form_submit_button("Roll"):
            ss.sim_msgs.append(sess.roll_position(int(pid), new_t)["msg"])


def risk_panel(sess: SimSession) -> None:
    st.subheader("Risk (USD)")
    rows = []
    for p, r in sess.risk.items():
        rows.append({"pair": p, "delta (base)": fm(r["delta_base"]), "delta USD": fm(r["delta_usd"]),
                     "gamma /1%": fm(r["gamma_usd"]), "vega /vol": fm(r["vega_usd"]), "theta /day": fm(r["theta_usd"]),
                     "vanna": fm(r["vanna_usd"]), "volga": fm(r["volga_usd"])})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    vb = pd.DataFrame({p: {t: r["vega_by_tenor_usd"].get(t, 0.0) for t in TENOR_LIST} for p, r in sess.risk.items()}).T
    vb = vb.loc[:, (vb.abs() > 1).any(axis=0)] if not vb.empty else vb
    if not vb.empty and vb.shape[1]:
        st.caption("Vega by tenor bucket (USD per vol pt)")
        st.dataframe(vb.map(fm), use_container_width=True)
    lim = pd.DataFrame(sess.limit_status())
    lim = lim[(lim["used"] > 0.25) | lim["breach"]]
    if not lim.empty:
        lim["status"] = np.where(lim["breach"], "🔴 BREACH", np.where(lim["used"] > 0.8, "🟠 near", "🟢"))
        lim["used"] = (lim["used"] * 100).round(0).astype(int).astype(str) + "%"
        lim["value_usd"] = lim["value_usd"].map(fm)
        lim["limit_usd"] = lim["limit_usd"].map(fm)
        st.caption("Limits")
        st.dataframe(lim[["pair", "limit", "value_usd", "limit_usd", "used", "status"]], hide_index=True,
                     use_container_width=True)
    else:
        st.caption("All limits under 25% used.")


def scenario_and_pnl(sess: SimSession) -> None:
    pairs_with_pos = [p for p in sess.book.pairs() if sess.book.legs(p)]
    c1, c2 = st.columns(2)
    with c1:
        if pairs_with_pos:
            p = st.selectbox("Scenario grid pair", pairs_with_pos, key="sg_pair")
            g = sess.scenario_grid(p)
            fig = go.Figure(go.Heatmap(z=g["pnl"], x=[f"{s:+d}%" for s in g["spots"]], y=[f"{v:+d}" for v in g["vols"]],
                                       colorscale="RdBu", zmid=0, text=[[fm(x) for x in row] for row in g["pnl"]],
                                       texttemplate="%{text}", showscale=False))
            fig.update_layout(title=f"{p} P&L (USD): spot move x vol move (pts)", height=300,
                              margin=dict(l=40, r=10, t=40, b=30), xaxis_title="spot", yaxis_title="vol")
            st.plotly_chart(fig, use_container_width=True, key="sgrid")
        else:
            st.caption("Scenario grid appears once you have positions.")
    with c2:
        h = np.array(sess.pnl_hist)
        fig = go.Figure(go.Scatter(x=h[:, 0], y=h[:, 1], mode="lines", line=dict(color="#2E6FD8")))
        fig.add_hline(y=0, line=dict(color="#999", dash="dot"))
        fig.update_layout(title="Intraday P&L (USD)", height=300, margin=dict(l=40, r=10, t=40, b=30),
                          xaxis_title="day", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True, key="pnlchart")


def news_panel(sess: SimSession) -> None:
    st.subheader("News")
    for n in sess.news[-6:][::-1]:
        icon = {"event": "📅", "jump": "⚡", "headline": "📰", "intervention": "🏛️", "regime": "🔀"}.get(n["kind"], "•")
        st.markdown(f"{icon} *day {n['t'] + 1:.2f}*: {n['text']}")
    up = sess.market.upcoming_events()
    if up:
        st.caption("Calendar: " + "; ".join(f"day {e['day'] + 1:.2f} {e['name']} ({e['ccy']}, priced ±{e['priced_sd_pct']:.2f}%)"
                                            for e in up[:5]))


def surface_tabs(sess: SimSession) -> None:
    tabs = st.tabs(["Vol surfaces", "Trade log", "Day debriefs"])
    with tabs[0]:
        pair = st.selectbox("Pair", sess.pairs, key="vs_pair")
        q = sess.market.quotes(pair)
        q0 = sess.market.state[pair].day_open_quotes
        fp = sess.market.forward_points(pair)
        rows, chg = [], []
        for t in TENOR_LIST:
            a, b = q[t], q0[t]
            rows.append({"Tenor": t, "ATM": a.atm * 100, "25RR": a.rr25 * 100, "25BF": a.bf25 * 100,
                         "10RR": a.rr10 * 100, "10BF": a.bf10 * 100, "Fwd pts": fp[t]})
            chg.append({"ATM": (a.atm - b.atm) * 100, "25RR": (a.rr25 - b.rr25) * 100, "25BF": (a.bf25 - b.bf25) * 100,
                        "10RR": (a.rr10 - b.rr10) * 100, "10BF": (a.bf10 - b.bf10) * 100})
        df = pd.DataFrame(rows).set_index("Tenor")
        ch = pd.DataFrame(chg, index=df.index)

        def color(col):
            if col.name not in ch:
                return [""] * len(col)
            return ["background-color: #d8f0e0" if v > 0.05 else "background-color: #f7d9d6" if v < -0.05 else ""
                    for v in ch[col.name]]
        st.dataframe(df.style.apply(color).format("{:.2f}"), use_container_width=True)
        st.caption(f"{get_pair(pair).convention_label()}. Green/red = up/down more than 0.05 vol since the day open. "
                   f"BF is the smile strangle.")
    with tabs[1]:
        if sess.trades:
            st.dataframe(pd.DataFrame([{"day": t["t"] + 1, "trade": t["desc"], "we": t["we"], "price": round(t["price"], 2),
                                        "fair": round(t["fair"], 2), "edge USD": round(t["edge_usd"]),
                                        "client": CLIENT_LABEL[t["client"]]} for t in sess.trades[::-1]]),
                         hide_index=True, use_container_width=True)
        else:
            st.caption("No client trades yet.")
    with tabs[2]:
        for d in sess.debriefs[::-1]:
            debrief_card(d)


def debrief_card(d: dict) -> None:
    t = d["terms"]
    with st.container(border=True):
        st.markdown(f"**Day {d['day']}: {fm(d['total'])} USD**. {d['takeaway']}")
        keys = ["delta", "gamma", "theta", "vega", "vanna", "volga", "edge", "hedge_cost", "carry", "unexplained"]
        fig = go.Figure(go.Bar(x=keys, y=[t[k] for k in keys],
                               marker_color=["#2A9D6F" if t[k] >= 0 else "#B8443A" for k in keys]))
        fig.update_layout(height=220, margin=dict(l=30, r=10, t=10, b=30), template="plotly_white")
        st.plotly_chart(fig, use_container_width=True, key=f"deb{d['day']}_{len(st.session_state.get('sim_msgs', []))}")
        if t["vega_by_tenor"]:
            st.caption("Vega P&L by tenor: " + ", ".join(f"{k} {fm(v)}" for k, v in t["vega_by_tenor"].items()))


def live_dashboard() -> None:
    import time
    sess: SimSession = ss.sim
    now = time.monotonic()
    # advance on wall-clock time only (button clicks also rerun this fragment)
    if not sess.market.finished and now - ss.get("sim_last_step", 0.0) >= 0.9 * CFG["tick_seconds"]:
        ss.sim_last_step = now
        sess.step()
        new = sess.new_log_entries()
        if new:
            db.log_events(ss.sim_id, new)
    if sess.market.finished:
        st.rerun()
    top_bar(sess)
    if sess.paused and sess.debriefs and sess.level == 1:
        st.info(f"Day {sess.debriefs[-1]['day']} done (auto-paused). {sess.debriefs[-1]['takeaway']} Press Resume to continue.")
    left, right = st.columns([1.1, 1])
    with left:
        rfq_panel(sess)
        hedge_panel(sess)
    with right:
        risk_panel(sess)
        news_panel(sess)
    scenario_and_pnl(sess)
    surface_tabs(sess)


# ---------------------------------------------------------------------------
# End of session
# ---------------------------------------------------------------------------
def end_screen() -> None:
    sess: SimSession = ss.sim
    card = scorecard(sess)
    if not ss.get("sim_saved"):
        db.log_events(ss.sim_id, sess.new_log_entries())
        db.finish_session(ss.sim_id, sess.pnl_usd, card)
        ss.sim_saved = True
    st.title("Session complete")
    st.caption(f"Seed {sess.seed} (replay with the same seed), level {sess.level}, regime **{sess.market.regime}**, "
               f"pairs {', '.join(sess.pairs)}")
    c = st.columns(5)
    c[0].metric("Total P&L (USD)", fm(card["total_pnl_usd"]))
    c[1].metric("Score after penalties", fm(card["score_usd"]))
    c[2].metric("Edge captured", fm(card["edge_captured_usd"]))
    c[3].metric("Fill rate", f"{card['fill_rate_pct']:.0f}%")
    c[4].metric("Informed-client P&L", fm(card["pnl_on_informed_client_trades_usd"]))
    c = st.columns(5)
    c[0].metric("Realised-vol luck (gamma+theta)", fm(card["realised_vol_luck_usd (gamma+theta)"]))
    c[1].metric("Vol moves (vega+vanna+volga)", fm(card["vol_moves_usd (vega+vanna+volga)"]))
    c[2].metric("Delta P&L", fm(card["delta_pnl_usd"]))
    c[3].metric("Hedging costs", fm(card["hedging_costs_usd"]))
    c[4].metric("Avg delta limit used", f"{card['avg_delta_limit_used_pct']:.0f}%")
    st.markdown(f"Limit breaches (ticks): {card['limit_breach_ticks'] or 'none'}. RFQs {card['rfqs']}, quoted "
                f"{card['quoted']}, traded {card['traded']}, passed {card['passed']}, missed {card['missed']}.")
    st.subheader("Review of your three most important decisions")
    if ss.get("sim_review") is None:
        with st.spinner("Writing the review..."):
            rv = claude_review(sess, card)
        ss.sim_review = rv or ("(No ANTHROPIC_API_KEY: rule-based review from the log.)\n\n" + rule_based_review(sess, card))
        db.update_review(ss.sim_id, ss.sim_review)
    st.markdown(ss.sim_review)
    st.subheader("Daily debriefs")
    for d in sess.debriefs:
        debrief_card(d)
    if st.button("New session", type="primary"):
        for k in ("sim", "sim_id", "sim_review", "sim_saved", "sim_msgs"):
            ss.pop(k, None)
        st.rerun()


# ---------------------------------------------------------------------------
if "sim" not in ss:
    setup_screen()
elif ss.sim.market.finished:
    end_screen()
else:
    st.fragment(run_every=CFG["tick_seconds"])(live_dashboard)()
    if st.sidebar.button("Abandon session"):
        for k in ("sim", "sim_id", "sim_review", "sim_saved", "sim_msgs"):
            ss.pop(k, None)
        st.rerun()

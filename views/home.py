"""Home: progress dashboard, weakest topics, recent sessions."""
import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from grading.llm import api_available
from progress import db

st.title("VolDesk")
st.caption("Options, rates and FX vol training. Every number comes from a tested engine; Claude only marks your writing.")

c = st.columns(4)
att = db.attempts(limit=5000)
c[0].metric("Questions answered", len(att))
c[1].metric("Average score", f"{pd.DataFrame(att)['final_score'].mean():.1f}/10" if att else "n/a")
sims = db.sessions(200)
c[2].metric("Simulator sessions", len([s for s in sims if s["finished"]]))
c[3].metric("Claude marking", "on" if api_available() else "off (self-mark)")
if not api_available():
    st.info("No ANTHROPIC_API_KEY found: written answers are self-marked against the engine model answer. "
            "Set the key and restart to enable Claude marking and session reviews.")

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Weakest topics (spaced repetition)")
    weak = db.weakest_topics(10)
    if weak:
        df = pd.DataFrame(weak)
        df["accuracy"] = (df["correct"] / df["seen"] * 100).round(0).astype(int).astype(str) + "%"
        st.dataframe(df[["section", "topic", "box", "seen", "accuracy"]], hide_index=True, use_container_width=True)
        st.caption("Leitner boxes: a pass (7+/10) moves a topic up a box, a fail sends it back to box 1. "
                   "Box 1 topics come back 16x as often as box 5 in Mixed review.")
    else:
        st.caption("Answer a few questions to see your weak spots here.")
    lt = db.leitner_table()
    if lt:
        counts = pd.DataFrame(lt).groupby("box").size().reindex(range(1, 6), fill_value=0)
        fig = go.Figure(go.Bar(x=[f"Box {b}" for b in counts.index], y=counts.values, marker_color="#2E6FD8"))
        fig.update_layout(title="Topics per Leitner box", height=260, margin=dict(l=30, r=10, t=40, b=30),
                          template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Recent results")
    if att:
        df = pd.DataFrame(att[:15])
        df["when"] = pd.to_datetime(df["ts"], unit="s").dt.strftime("%d %b %H:%M")
        st.dataframe(df[["when", "subsection", "topic", "difficulty", "final_score"]], hide_index=True,
                     use_container_width=True)
        by = pd.DataFrame(att).groupby("subsection")["final_score"].agg(["count", "mean"]).round(1)
        st.caption("By sub-section")
        st.dataframe(by, use_container_width=True)
    st.subheader("Recent simulator sessions")
    fin = [s for s in sims if s["finished"]][:8]
    if fin:
        rows = []
        for s in fin:
            card = json.loads(s["scorecard_json"] or "{}")
            rows.append({"when": pd.to_datetime(s["ts"], unit="s").strftime("%d %b %H:%M"), "level": s["level"],
                         "regime": s["regime"], "P&L USD": round(s["total_pnl_usd"] or 0),
                         "score USD": round(card.get("score_usd", 0)), "fill %": round(card.get("fill_rate_pct", 0))})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    else:
        st.caption("No finished sessions yet.")

st.subheader("Where to start")
st.markdown("- **Interview Prep: Options**: 1B (write your exposures) is the core drill. Start at difficulty 1.\n"
            "- **Interview Prep: Rates**: work through 2A stage by stage; each unlocks the next.\n"
            "- **FX Vol Simulator**: Level 1 first. It pauses at each day end so you can read the debrief.\n"
            "- **Engine Lab**: inspect the vol surfaces and price options yourself; plug in your own pricer.")

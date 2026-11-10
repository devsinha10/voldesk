"""Past simulator sessions: scorecard, review and full event log."""
import json

import pandas as pd
import streamlit as st

from progress import db

st.title("Session History")
sims = db.sessions(200)
if not sims:
    st.caption("No simulator sessions yet.")
    st.stop()
labels = [f"#{s['id']}  {pd.to_datetime(s['ts'], unit='s'):%d %b %H:%M}  L{s['level']}  {s['regime']}  "
          f"seed {s['seed']}  {'P&L ' + format(round(s['total_pnl_usd'] or 0), ',') + ' USD' if s['finished'] else '(unfinished)'}"
          for s in sims]
i = st.selectbox("Session", range(len(sims)), format_func=lambda k: labels[k])
s = sims[i]
st.caption(f"Replay this market with seed **{s['seed']}** at level {s['level']} "
           f"(set the regime to '{s['regime']}' under Practice options to match exactly).")
if s["scorecard_json"]:
    card = json.loads(s["scorecard_json"])
    flat = {k: v for k, v in card.items() if not isinstance(v, (dict, list))}
    st.dataframe(pd.DataFrame([flat]).T.rename(columns={0: "value"}), use_container_width=True)
if s["review_text"]:
    st.subheader("Review")
    st.markdown(s["review_text"])
ev = db.session_events(s["id"])
st.subheader(f"Event log ({len(ev)} events)")
kinds = sorted({e["kind"] for e in ev})
pick = st.multiselect("Show", kinds, default=[k for k in kinds if k not in ("rfq",)])
rows = [e for e in ev if e["kind"] in pick]
if rows:
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True, height=420)
st.download_button("Download log (JSON)", json.dumps(ev, default=str, indent=1), file_name=f"session_{s['id']}.json")

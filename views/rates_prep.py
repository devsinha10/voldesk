"""Section 2: Interview Prep (Rates)."""
import streamlit as st

import prep_rates as pr
from progress import db
from progress.review import mixed_review
from ui.components import question_page

st.title("Interview Prep: Rates")
st.caption("Duration and convexity built up in stages. Calculations only appear inside desk scenarios; "
           "every number is a full revaluation on the engine's curve.")
unlock_all = st.sidebar.checkbox("Unlock all 2A stages", value=False)
locked = pr.locked_stages(db.stage_stats, unlock_all)
with st.expander("2A progress"):
    for code, (title, _) in list(pr.SUBSECTIONS.items())[:5]:
        s = db.stage_stats(code)
        st.write(f"{'🔒' if code in locked else '✅'} **{code}** {title}: {s['n']} attempts, avg {s['avg']:.1f}/10")

subs = {k: v for k, v in pr.SUBSECTIONS.items()}
gens = [v[1] for k, v in pr.SUBSECTIONS.items() if k not in locked]
question_page("rates", "rates", subs, review_pool=lambda seed, d: mixed_review(gens, "rates", seed, d),
              locked=locked)

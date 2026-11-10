"""Section 1: Interview Prep (Options)."""
import streamlit as st

import prep_options as po
from progress.review import mixed_review
from ui.components import question_page

st.title("Interview Prep: Options")
st.caption("Every number below comes from the pricing engine. Claude only marks your written answers.")

subs = {k: (v[0], v[1]) for k, v in po.SUBSECTIONS.items()}
gens = [v[1] for v in po.SUBSECTIONS.values()]
question_page("opt", "options", subs, review_pool=lambda seed, d: mixed_review(gens, "options", seed, d))

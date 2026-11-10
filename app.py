"""VolDesk: Streamlit entry point."""
import streamlit as st

st.set_page_config(page_title="VolDesk", page_icon="📈", layout="wide")

pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/options_prep.py", title="Interview Prep: Options", icon="🧮"),
    st.Page("views/rates_prep.py", title="Interview Prep: Rates", icon="📉"),
    st.Page("views/simulator.py", title="FX Vol Simulator", icon="💱"),
    st.Page("views/history.py", title="Session History", icon="🗂️"),
    st.Page("views/engine_lab.py", title="Engine Lab", icon="🔬"),
]
st.navigation(pages).run()

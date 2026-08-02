import streamlit as st
from ui.views import load_css

st.set_page_config(
    page_title="FinSuite Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# Definisci le pagine
historical_page = st.Page("pages_app/historical.py", title="Analisi Storica", icon="📈")
simulator_page = st.Page("pages_app/simulator.py", title="Portfolio Simulator", icon="🎲")

pg = st.navigation([simulator_page, historical_page])
pg.run()

import streamlit as st
import os

from engine.config import ASSET_CATALOG
from engine.data_fetcher import fetch_asset_data, calculate_moving_average
from ui.views import load_css, render_sidebar, render_main_dashboard

def main() -> None:
    # Configurazione della pagina
    st.set_page_config(
        page_title="Dashboard Finanziaria",
        page_icon="📈",
        layout="wide"
    )
    
    # Carica CSS personalizzato
    css_path = os.path.join(os.path.dirname(__file__), "ui", "style.css")
    load_css(css_path)
    
    # Rendering Sidebar con navigazione gerarchica
    selected_ticker, asset_name = render_sidebar(ASSET_CATALOG)
    
    # Rendering Principale
    render_main_dashboard(
        ticker=selected_ticker,
        asset_name=asset_name,
        fetch_func=fetch_asset_data,
        calc_ma_func=calculate_moving_average
    )

if __name__ == "__main__":
    main()

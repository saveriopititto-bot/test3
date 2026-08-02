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
    
    # Carica CSS personalizzato per Milligram e colori custom
    css_path = os.path.join(os.path.dirname(__file__), "ui", "style.css")
    load_css(css_path)
    
    # Rendering Sidebar
    selected_ticker = render_sidebar(ASSET_CATALOG)
    asset_name = ASSET_CATALOG.get(selected_ticker, "Sconosciuto")
    
    # Rendering Principale (Separazione netta: passo solo i dati e le funzioni pure)
    render_main_dashboard(
        ticker=selected_ticker,
        asset_name=asset_name,
        fetch_func=fetch_asset_data,
        calc_ma_func=calculate_moving_average
    )

if __name__ == "__main__":
    main()

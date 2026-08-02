import streamlit as st
from config.settings import ASSET_CATALOG
from data.fetcher import fetch_asset_data, calculate_moving_average
from ui.views import load_css, render_sidebar, render_main_dashboard

# --- MAIN APP ---
def main() -> None:
    st.set_page_config(
        page_title="Dashboard Finanziaria",
        page_icon="📈",
        layout="wide"
    )
    
    load_css()
    
    selected_ticker, asset_name, selected_period = render_sidebar(ASSET_CATALOG)
    
    render_main_dashboard(
        ticker=selected_ticker,
        asset_name=asset_name,
        period=selected_period,
        fetch_func=fetch_asset_data,
        calc_ma_func=calculate_moving_average
    )

if __name__ == "__main__":
    main()

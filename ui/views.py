import os
import streamlit as st
from typing import Dict, Tuple, Callable
from ui.charts import create_price_chart

def load_css() -> None:
    css_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'style.css'))
    try:
        with open(css_path, 'r') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("File style.css non trovato.")

def render_sidebar(catalog: Dict[str, Dict[str, Dict[str, str]]]) -> Tuple[str, str]:
    st.sidebar.title("🛠️ Filtri e Selezione")
    
    st.sidebar.markdown("### 1. Mercato")
    markets = list(catalog.keys())
    selected_market = st.sidebar.selectbox("Seleziona Area Geografica", markets, label_visibility="collapsed")
    
    st.sidebar.markdown("### 2. Categoria")
    # type: ignore
    categories = list(catalog[selected_market].keys())
    selected_category = st.sidebar.selectbox("Seleziona Classe di Investimento", categories, label_visibility="collapsed")
    
    st.sidebar.markdown("### 3. Strumento Finanziario")
    assets = catalog[selected_market][selected_category]
    options = {ticker: f"{name} ({ticker})" for ticker, name in assets.items()}
    
    selected_ticker = st.sidebar.selectbox(
        "Seleziona Ticker",
        options=list(options.keys()),
        format_func=lambda x: options[x],
        label_visibility="collapsed"
    )
    
    return str(selected_ticker), assets[str(selected_ticker)]

def render_main_dashboard(ticker: str, asset_name: str, fetch_func: Callable, calc_ma_func: Callable) -> None:
    st.title(f"📊 Analisi: {asset_name}")
    st.markdown(f"Visualizzazione dati storici per il ticker **{ticker}**.")
    
    with st.spinner("Sincronizzazione dati in corso..."):
        df = fetch_func(ticker)
        
        if df.empty:
            st.error("Nessun dato disponibile per l'asset selezionato (potrebbe essere un ticker non valido o delistato).")
            return
            
        df_processed = calc_ma_func(df, window=30)
        
        tab_chart, tab_data = st.tabs(["📉 Grafico Interattivo", "🗂️ Dati Tabellari"])
        
        with tab_chart:
            st.markdown(f"#### Serie Storica")
            fig = create_price_chart(df_processed, ticker, asset_name)
            st.plotly_chart(fig, use_container_width=True)
            
        with tab_data:
            st.markdown("#### Tabella Dati Recenti")
            display_df = df_processed.tail(30).sort_index(ascending=False)
            st.dataframe(display_df, use_container_width=True)

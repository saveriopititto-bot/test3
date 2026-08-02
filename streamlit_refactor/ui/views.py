import streamlit as st
import pandas as pd
from typing import Dict, Callable, Any, Tuple
from ui.charts import create_price_chart

def load_css(file_name: str) -> None:
    """
    Carica il file CSS specificato e lo inietta in Streamlit.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Attenzione: Impossibile trovare il file di stile: {file_name}")

def render_sidebar(catalog: Dict[str, Dict[str, Dict[str, str]]]) -> Tuple[str, str]:
    """
    Renderizza la sidebar per la navigazione gerarchica.
    Ritorna una tupla con (ticker, nome dell'asset).
    """
    st.sidebar.title("🛠️ Filtri e Selezione")
    
    # 1. Scelta Mercato
    st.sidebar.markdown("### 1. Mercato")
    markets = list(catalog.keys())
    selected_market = st.sidebar.selectbox("Seleziona Area Geografica", markets, label_visibility="collapsed")
    
    # 2. Scelta Categoria
    st.sidebar.markdown("### 2. Categoria")
    # type: ignore
    categories = list(catalog[selected_market].keys())
    selected_category = st.sidebar.selectbox("Seleziona Classe di Investimento", categories, label_visibility="collapsed")
    
    # 3. Scelta Asset
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
    """
    Gestisce il layout principale delegando il recupero dati alle funzioni passate.
    """
    st.title(f"📊 Analisi: {asset_name}")
    st.markdown(f"Visualizzazione dati storici per il ticker **{ticker}**.")
    
    # Fetch Data
    with st.spinner("Sincronizzazione dati in corso..."):
        df = fetch_func(ticker)
        
        if df.empty:
            st.error("Nessun dato disponibile per l'asset selezionato (potrebbe essere un ticker non valido o delistato).")
            return
            
        # Calcolo logica di business
        df_processed = calc_ma_func(df, window=30)
        
        # Tabs Layout
        tab_chart, tab_data = st.tabs(["📉 Grafico Interattivo", "🗂️ Dati Tabellari"])
        
        with tab_chart:
            st.markdown(f"#### Serie Storica")
            fig = create_price_chart(df_processed, ticker, asset_name)
            st.plotly_chart(fig, use_container_width=True)
            
        with tab_data:
            st.markdown("#### Tabella Dati Recenti")
            display_df = df_processed.tail(30).sort_index(ascending=False)
            st.dataframe(display_df, use_container_width=True)

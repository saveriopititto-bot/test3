import streamlit as st
import pandas as pd
from typing import Dict, Callable
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

def render_sidebar(catalog: Dict[str, str]) -> str:
    """
    Renderizza la sidebar per la navigazione e ritorna il ticker selezionato.
    """
    st.sidebar.title("Opzioni Dashboard")
    st.sidebar.markdown("Seleziona un asset per visualizzare la serie storica.")
    
    # Costruisci opzioni dropdown combinate (Nome + Ticker)
    options = {ticker: f"{name} ({ticker})" for ticker, name in catalog.items()}
    
    selected_ticker = st.sidebar.selectbox(
        "Seleziona Asset",
        options=list(options.keys()),
        format_func=lambda x: options[x]
    )
    
    return str(selected_ticker)

def render_main_dashboard(ticker: str, asset_name: str, fetch_func: Callable, calc_ma_func: Callable) -> None:
    """
    Gestisce il layout principale delegando il recupero dati alle funzioni passate.
    """
    st.title(f"📊 Analisi Asset: {asset_name}")
    st.markdown(f"Visualizzazione dati storici per il ticker **{ticker}**.")
    
    # Fetch Data
    with st.spinner("Sincronizzazione dati in corso..."):
        df = fetch_func(ticker)
        
        if df.empty:
            st.error("Nessun dato disponibile per l'asset selezionato.")
            return
            
        # Calcolo logica di business
        df_processed = calc_ma_func(df, window=30)
        
        # Tabs Layout
        tab_chart, tab_data = st.tabs(["📉 Grafico Interattivo", "🗂️ Dati Tabellari"])
        
        with tab_chart:
            st.markdown(f"#### Serie Storica - Ultimo Anno")
            fig = create_price_chart(df_processed, ticker, asset_name)
            st.plotly_chart(fig, use_container_width=True)
            
        with tab_data:
            st.markdown("#### Tabella Dati Recenti")
            # Mostriamo gli ultimi 30 giorni pulendo i nomi delle colonne
            display_df = df_processed.tail(30).sort_index(ascending=False)
            st.dataframe(display_df, use_container_width=True)

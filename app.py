import streamlit as st
import yfinance as yf
import pandas as pd

# Configurazione della pagina
st.set_page_config(page_title="Monitoraggio Futures", layout="wide")
st.title("📈 Dashboard Andamento Futures (Beta)")

# Funzione di recupero dati con cache per non sovraccaricare le richieste
@st.cache_data(ttl=900)
def scarica_dati_future(ticker, periodo="1mo"):
    asset = yf.Ticker(ticker)
    storico = asset.history(period=periodo)
    
    if not storico.empty:
        storico.reset_index(inplace=True)
        
        # 1. Uniforma il nome della colonna (yfinance a volte usa 'Datetime' per periodi brevi)
        if 'Datetime' in storico.columns:
            storico.rename(columns={'Datetime': 'Date'}, inplace=True)
            
        # 2. LA SOLUZIONE AL BUG: Forza il formato a data semplice, rimuovendo il fuso orario
        storico['Date'] = pd.to_datetime(storico['Date']).dt.date
        
    return storico

# Mappatura etichette comprensibili -> Ticker di Yahoo Finance
futures_disponibili = {
    "S&P 500 (USA)": "ES=F",
    "Nasdaq 100 (USA)": "NQ=F",
    "Petrolio WTI": "CL=F",
    "Oro": "GC=F",
    "Euro/Dollaro": "6E=F",
    "Borsa Italiana (ETF)": "EWI"
}

# Layout dell'interfaccia con due colonne per i filtri
col1, col2 = st.columns(2)

with col1:
    scelta = st.selectbox("Seleziona il Future:", list(futures_disponibili.keys()))

with col2:
    periodo_scelto = st.selectbox("Orizzonte temporale:", ["5d", "1mo", "3mo", "6mo", "1y", "5y", "10y"], index=1)

ticker_selezionato = futures_disponibili[scelta]

# Scaricamento dati con feedback visivo (spinner)
with st.spinner(f"Scaricamento dati per {scelta}..."):
    dati = scarica_dati_future(ticker_selezionato, periodo=periodo_scelto)

# Visualizzazione della dashboard
if not dati.empty:
    st.subheader(f"Prezzo di chiusura: {scelta} ({ticker_selezionato})")
    
    # Grafico a linee nativo di Streamlit
    st.line_chart(data=dati, x="Date", y="Close", height=450, use_container_width=True)
    
    st.subheader("Ultimi valori registrati")
    # Tabella degli ultimi 10 giorni, partendo dal più recente
    dati_ordinati = dati.sort_values(by="Date", ascending=False).head(10)
    st.dataframe(dati_ordinati, use_container_width=True)
    
else:
    st.error("Nessun dato disponibile al momento per questo ticker. I mercati potrebbero essere chiusi o il ticker non è valido.")

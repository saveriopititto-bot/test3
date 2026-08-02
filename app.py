import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 1. Configurazione della pagina
st.set_page_config(page_title="Monitoraggio Futures", layout="wide")
st.title("📈 Dashboard Andamento Futures (Beta)")

# 2. Funzione di recupero e pulizia dati (con cache)
@st.cache_data(ttl=900)
def scarica_dati_future(ticker, periodo="1mo"):
    asset = yf.Ticker(ticker)
    storico = asset.history(period=periodo)
    
    if not storico.empty:
        storico.reset_index(inplace=True)
        
        # Uniforma il nome della colonna in caso di periodi intraday
        if 'Datetime' in storico.columns:
            storico.rename(columns={'Datetime': 'Date'}, inplace=True)
            
        # Pulisce la data rimuovendo il fuso orario per evitare bug grafici
        storico['Date'] = pd.to_datetime(storico['Date']).dt.date
        
    return storico

# 3. Mappatura Ticker
futures_disponibili = {
    "S&P 500 (USA)": "ES=F",
    "Nasdaq 100 (USA)": "NQ=F",
    "Petrolio WTI": "CL=F",
    "Oro": "GC=F",
    "Euro/Dollaro": "6E=F",
    "Borsa Italiana (ETF)": "EWI"
}

# 4. Interfaccia utente: Filtri su tre colonne
col1, col2, col3 = st.columns(3)

with col1:
    scelta = st.selectbox("Seleziona il Future:", list(futures_disponibili.keys()))

with col2:
    periodo_scelto = st.selectbox("Orizzonte temporale:", ["5d", "1mo", "3mo", "6mo", "1y", "5y", "10y"], index=4)

with col3:
    # Selezione della Media Mobile
    opzioni_ma = {"Nessuna": 0, "SMA 20 giorni": 20, "SMA 50 giorni": 50, "SMA 200 giorni": 200}
    scelta_ma = st.selectbox("Aggiungi Media Mobile:", list(opzioni_ma.keys()))
    periodi_ma = opzioni_ma[scelta_ma]

ticker_selezionato = futures_disponibili[scelta]

# 5. Scaricamento ed elaborazione dati
with st.spinner(f"Scaricamento dati per {scelta}..."):
    dati = scarica_dati_future(ticker_selezionato, periodo=periodo_scelto)

if not dati.empty:
    st.subheader(f"Prezzo di chiusura: {scelta} ({ticker_selezionato})")
    
    # 6. Calcolo della Media Mobile (se selezionata)
    colonne_da_plottare = ["Close"]
    
    if periodi_ma > 0:
        nome_colonna_ma = f"Media Mobile ({periodi_ma} gg)"
        # Calcola la media mobile sui prezzi di chiusura
        dati[nome_colonna_ma] = dati["Close"].rolling(window=periodi_ma).mean()
        colonne_da_plottare.append(nome_colonna_ma)
        
        # Avviso se l'orizzonte temporale è troppo breve per calcolare la media
        if len(dati) < periodi_ma:
            st.warning(f"Attenzione: L'orizzonte temporale scelto ({len(dati)} giorni disponibili) è troppo breve per calcolare una media mobile a {periodi_ma} giorni. Aumenta l'orizzonte temporale.")

    # 7. Creazione del grafico con Plotly
    fig = px.line(
        dati, 
        x="Date", 
        y=colonne_da_plottare,
        color_discrete_sequence=["#1f77b4", "#ff7f0e"] # Colore blu per il prezzo, arancione per la media
    )
    
    # Ottimizzazione del layout del grafico
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Prezzo",
        legend_title_text=None,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), # Legenda in alto
        xaxis=dict(
            tickformat="%Y", 
            dtick="M12" if periodo_scelto in ["5y", "10y"] else None
        )
    )
    
    # Renderizza il grafico in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # 8. Tabella dati
    st.subheader("Ultimi valori registrati")
    dati_ordinati = dati.sort_values(by="Date", ascending=False).head(10)
    st.dataframe(dati_ordinati, use_container_width=True)
    
else:
    st.error("Nessun dato disponibile al momento per questo ticker.")

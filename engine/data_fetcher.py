import yfinance as yf
import pandas as pd
from typing import Optional

def fetch_asset_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Recupera i dati storici per un dato ticker utilizzando yfinance.
    La logica è puramente funzionale e non dipende da Streamlit.
    """
    try:
        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        print(f"Errore nel recupero dati per {ticker}: {e}")
        return pd.DataFrame()

def calculate_moving_average(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """
    Calcola la media mobile per la colonna 'Close' di un DataFrame.
    Gestisce automaticamente l'output multi-index di yfinance.
    """
    if df.empty or 'Close' not in df.columns:
        return df
    
    df_result = df.copy()
    
    # Flatten multi-index per compatibilità yfinance >= 0.2.30
    if isinstance(df_result.columns, pd.MultiIndex):
        close_col = df_result['Close'].iloc[:, 0]
    else:
        close_col = df_result['Close']
        
    df_result[f'MA_{window}'] = close_col.rolling(window=window).mean()
    return df_result

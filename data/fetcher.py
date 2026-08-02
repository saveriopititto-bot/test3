import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_asset_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Recupera i dati storici per un dato ticker utilizzando yfinance.
    Gestisce periodi personalizzati convertendoli in date di inizio e fine.
    """
    try:
        end_date = datetime.now()
        
        if period == "1w":
            start_date = end_date - timedelta(weeks=1)
        elif period == "2w":
            start_date = end_date - timedelta(weeks=2)
        elif period == "1mo":
            start_date = end_date - timedelta(days=30)
        elif period == "3mo":
            start_date = end_date - timedelta(days=90)
        elif period == "6mo":
            start_date = end_date - timedelta(days=180)
        elif period == "1y":
            start_date = end_date - timedelta(days=365)
        elif period == "3y":
            start_date = end_date - timedelta(days=365*3)
        elif period == "5y":
            start_date = end_date - timedelta(days=365*5)
        else:
            # Fallback per qualsiasi altro periodo, usando il parametro period nativo
            data = yf.download(ticker, period=period, progress=False)
            if data.empty:
                return pd.DataFrame()
            return data
            
        data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
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
    
    if isinstance(df_result.columns, pd.MultiIndex):
        close_col = df_result['Close'].iloc[:, 0]
    else:
        close_col = df_result['Close']
        
    df_result[f'MA_{window}'] = close_col.rolling(window=window).mean()
    return df_result

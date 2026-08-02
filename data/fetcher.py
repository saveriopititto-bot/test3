import yfinance as yf
import pandas as pd

def fetch_asset_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Recupera i dati storici per un dato ticker utilizzando yfinance.
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
    
    if isinstance(df_result.columns, pd.MultiIndex):
        close_col = df_result['Close'].iloc[:, 0]
    else:
        close_col = df_result['Close']
        
    df_result[f'MA_{window}'] = close_col.rolling(window=window).mean()
    return df_result

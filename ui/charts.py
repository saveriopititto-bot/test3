import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_price_chart(df: pd.DataFrame, ticker: str, asset_name: str) -> go.Figure:
    """
    Crea un grafico Plotly interattivo per i prezzi di chiusura e le medie mobili.
    """
    if df.empty:
        return go.Figure()

    # Gestione compatibilità MultiIndex pandas/yfinance
    if isinstance(df.columns, pd.MultiIndex):
        close_series = df['Close'].iloc[:, 0]
    else:
        close_series = df['Close']

    fig = go.Figure()
    
    # Aggiungi traccia Prezzo di Chiusura
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=close_series, 
            mode='lines', 
            name='Prezzo Chiusura', 
            line=dict(color='#035158') # Blu Petrolio
        )
    )
    
    # Identifica e aggiungi le medie mobili se presenti
    for col in df.columns:
        if isinstance(col, tuple):
            col_name = col[0]
        else:
            col_name = col
            
        if isinstance(col_name, str) and col_name.startswith('MA_'):
            ma_series = df[col] if not isinstance(df.columns, pd.MultiIndex) else df[col].iloc[:, 0] if isinstance(df[col], pd.DataFrame) else df[col]
            fig.add_trace(
                go.Scatter(
                    x=df.index, 
                    y=ma_series, 
                    mode='lines', 
                    name=col_name, 
                    line=dict(dash='dash', color='#e5eff0')
                )
            )
            
    fig.update_layout(
        title=f"Andamento Prezzo: {asset_name} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Prezzo (USD)",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

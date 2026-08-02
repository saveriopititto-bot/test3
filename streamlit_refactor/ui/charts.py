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
    
    # Colori allineati alla nuova palette funzionale
    primary_line_color = '#635BFF' # Vibrant Indigo per evidenziare il prezzo
    ma_colors = ['#00D09C', '#F04438', '#F6C343'] # Verde Menta, Rosso, Giallo
    
    # Aggiungi traccia Prezzo di Chiusura
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=close_series, 
            mode='lines', 
            name='Prezzo Chiusura', 
            line=dict(color=primary_line_color, width=2)
        )
    )
    
    # Identifica e aggiungi le medie mobili se presenti
    ma_index = 0
    for col in df.columns:
        if isinstance(col, tuple):
            col_name = col[0]
        else:
            col_name = col
            
        if isinstance(col_name, str) and col_name.startswith('MA_'):
            ma_series = df[col] if not isinstance(df.columns, pd.MultiIndex) else df[col].iloc[:, 0] if isinstance(df[col], pd.DataFrame) else df[col]
            ma_color = ma_colors[ma_index % len(ma_colors)]
            fig.add_trace(
                go.Scatter(
                    x=df.index, 
                    y=ma_series, 
                    mode='lines', 
                    name=col_name, 
                    line=dict(dash='dash', color=ma_color, width=1.5)
                )
            )
            ma_index += 1
            
    fig.update_layout(
        title=f"Andamento Storico: {asset_name} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Prezzo",
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

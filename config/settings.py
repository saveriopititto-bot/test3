from typing import Dict

# Palette di brand condivisa tra CSS (assets/style.css) e i grafici Plotly,
# cosi' i colori restano coerenti su tutta l'app.
CHART_COLORS: Dict[str, str] = {
    "primary": "#0A2540",
    "secondary": "#635BFF",
    "tertiary": "#4F566B",
    "positive": "#00D09C",
    "negative": "#F04438",
    "warning": "#F6C343",
    "stocks": "#635BFF",
    "bonds": "#0A2540",
    "cash": "#00D09C",
    "range_fill": "rgba(99, 91, 255, 0.15)",
}

ASSET_CATALOG: Dict[str, Dict[str, Dict[str, str]]] = {
    "Mercato USA": {
        "Azionario (Indici)": {
            "SPY": "S&P 500 ETF",
            "QQQ": "Nasdaq 100 ETF",
            "URTH": "MSCI All World ETF"
        },
        "Obbligazionario": {
            "TLT": "iShares 20+ Year Treasury Bond",
            "AGG": "iShares Core US Aggregate Bond",
            "BND": "Vanguard Total Bond Market"
        },
        "Commodities Alimentari": {
            "CORN": "Teucrium Corn Fund",
            "WEAT": "Teucrium Wheat Fund",
            "SOYB": "Teucrium Soybean Fund",
            "DBA": "Invesco DB Agriculture Fund"
        }
    },
    "Mercato Italia / Europa": {
        "Azionario (Indici)": {
            "EWI": "iShares MSCI Italy ETF",
            "EXSA.DE": "STOXX Europe 600 ETF",
            "URTH": "MSCI All World ETF"
        },
        "Obbligazionario": {
            "XG7S.MI": "Xtrackers Eurozone Gov Bond 7-10",
            "IBTS.AS": "iShares Euro Treasury Bond 1-3yr",
            "SEGA.MI": "iShares Core Global Aggregate Bond"
        },
        "Commodities Alimentari": {
            "CORN": "Teucrium Corn Fund",
            "WEAT": "Teucrium Wheat Fund",
            "SOYB": "Teucrium Soybean Fund",
            "DBA": "Invesco DB Agriculture Fund"
        }
    }
}

from typing import Dict, Any

# Catalogo Strutturato per Mercato -> Categoria -> Asset
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

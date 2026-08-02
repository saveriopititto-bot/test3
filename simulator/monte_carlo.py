import numpy as np
import pandas as pd

def run_monte_carlo(
    initial_investment: float,
    annual_contribution: float,
    years: int,
    alloc_stocks: float,
    alloc_bonds: float,
    alloc_cash: float,
    n_simulations: int = 500
) -> pd.DataFrame:
    """
    Esegue una simulazione Monte Carlo vettorializzata per un portafoglio.
    Ritorna un DataFrame (years + 1, n_simulations) con il valore del portafoglio in ogni anno.
    """
    # Parametri storici ipotetici (Rendimento atteso e volatilità)
    mu_s, sigma_s = 0.08, 0.15   # Azioni
    mu_b, sigma_b = 0.04, 0.05   # Obbligazioni
    mu_c, sigma_c = 0.02, 0.01   # Liquidità
    
    # Normalizza pesi per sicurezza
    total_w = alloc_stocks + alloc_bonds + alloc_cash
    if total_w == 0:
        w_s, w_b, w_c = 0, 0, 1
    else:
        w_s = alloc_stocks / total_w
        w_b = alloc_bonds / total_w
        w_c = alloc_cash / total_w
        
    # Calcolo portafoglio atteso e volatilità
    # Assumiamo una correlazione stock-bond di 0.1, le altre a zero
    corr_sb = 0.1
    
    mu_p = w_s * mu_s + w_b * mu_b + w_c * mu_c
    var_p = (w_s**2 * sigma_s**2) + (w_b**2 * sigma_b**2) + (w_c**2 * sigma_c**2) + (2 * w_s * w_b * sigma_s * sigma_b * corr_sb)
    sigma_p = np.sqrt(var_p)
    
    # Genera rendimenti casuali normali per tutti gli anni e tutte le simulazioni
    # R ~ N(mu_p, sigma_p^2)
    random_returns = np.random.normal(mu_p, sigma_p, (years, n_simulations))
    
    # Inizializza array valori portafoglio
    portfolio_values = np.zeros((years + 1, n_simulations))
    portfolio_values[0] = initial_investment
    
    for t in range(1, years + 1):
        # Il valore cresce del rendimento casuale e si aggiunge il contributo (a fine anno)
        portfolio_values[t] = portfolio_values[t-1] * (1 + random_returns[t-1]) + annual_contribution
        
    return pd.DataFrame(portfolio_values)

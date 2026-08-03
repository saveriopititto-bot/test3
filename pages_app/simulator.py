import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from simulator.monte_carlo import run_monte_carlo
from config.settings import CHART_COLORS

# Callback per sincronizzare i profili di rischio con gli slider
def update_sliders_from_profile():
    profile = st.session_state.risk_profile
    if profile == "Conservative":
        st.session_state.s_stocks = 20
        st.session_state.s_bonds = 70
        st.session_state.s_cash = 10
    elif profile == "Balanced":
        st.session_state.s_stocks = 60
        st.session_state.s_bonds = 35
        st.session_state.s_cash = 5
    elif profile == "Aggressive":
        st.session_state.s_stocks = 90
        st.session_state.s_bonds = 10
        st.session_state.s_cash = 0

def run():
    # Inizializza session state
    if 's_stocks' not in st.session_state:
        st.session_state.s_stocks = 60
        st.session_state.s_bonds = 35
        st.session_state.s_cash = 5
        st.session_state.risk_profile = "Balanced"
        
    st.sidebar.markdown("### INITIAL INVESTMENT")
    init_inv = st.sidebar.number_input("", value=25000, step=1000, label_visibility="collapsed")
    
    st.sidebar.markdown("### ANNUAL CONTRIBUTION")
    ann_cont = st.sidebar.number_input("", value=6000, step=500, key="ann_cont", label_visibility="collapsed")
    
    st.sidebar.markdown("### YEARS HORIZON")
    years = st.sidebar.slider("", min_value=1, max_value=50, value=20, label_visibility="collapsed")
    
    st.sidebar.markdown("### RISK PROFILE")
    st.sidebar.radio(
        "", 
        options=["Conservative", "Balanced", "Aggressive"], 
        key="risk_profile", 
        on_change=update_sliders_from_profile,
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### ALLOCATION")
    stocks = st.sidebar.slider("Stocks", 0, 100, key="s_stocks")
    bonds = st.sidebar.slider("Bonds", 0, 100, key="s_bonds")
    cash = st.sidebar.slider("Cash", 0, 100, key="s_cash")
    
    # Normalizza se diverso da 100
    tot = stocks + bonds + cash
    if tot != 100 and tot != 0:
        stocks = stocks / tot * 100
        bonds = bonds / tot * 100
        cash = cash / tot * 100

    st.sidebar.markdown("### SIMULATIONS")
    n_sims = st.sidebar.slider("", min_value=100, max_value=2000, step=100, value=500, label_visibility="collapsed")
    
    run_btn = st.sidebar.button("▶ Run simulation", use_container_width=True, type="primary")

    st.title("Portfolio Simulator")
    st.markdown("Monte Carlo retirement scenarios")
    
    # Esecuzione simulazione
    df_sim = run_monte_carlo(init_inv, ann_cont, years, stocks, bonds, cash, n_sims)
    
    # Calcolo Metriche all'ultimo anno
    final_values = df_sim.iloc[-1].values
    median_val = np.median(final_values)
    p90_val = np.percentile(final_values, 90)
    p10_val = np.percentile(final_values, 10)
    
    total_contributed = init_inv + (ann_cont * years)
    prob_loss = np.mean(final_values < total_contributed) * 100
    
    # Formattazione per le card
    def fmt(val): return f"${val/1000:.1f}K"
    def delta(val): return f"+ ${max(0, val - total_contributed)/1000:.1f}K vs contributed"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Median Outcome</div><div class="metric-value">{fmt(median_val)}</div><div class="metric-delta">▲ {delta(median_val)}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">90th Percentile</div><div class="metric-value">{fmt(p90_val)}</div><div class="metric-delta">▲ {delta(p90_val)}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">10th Percentile</div><div class="metric-value">{fmt(p10_val)}</div><div class="metric-delta">▲ {delta(p10_val)}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Probability of Loss</div><div class="metric-value">{prob_loss:.0f}%</div><div class="metric-delta metric-delta-neutral">below contributions</div></div>', unsafe_allow_html=True)
    
    st.write("")
    
    # Grafico Linea
    fig_line = go.Figure()
    x_axis = np.arange(years + 1)
    
    # Mediana
    medians = df_sim.median(axis=1)
    p10 = df_sim.quantile(0.10, axis=1)
    p90 = df_sim.quantile(0.90, axis=1)
    contributions = [init_inv + (ann_cont * t) for t in x_axis]
    
    fig_line.add_trace(go.Scatter(
        x=np.concatenate([x_axis, x_axis[::-1]]),
        y=np.concatenate([p90, p10[::-1]]),
        fill='toself',
        fillcolor=CHART_COLORS["range_fill"],
        line=dict(color='rgba(255,255,255,0)'),
        name='10-90% range'
    ))

    fig_line.add_trace(go.Scatter(x=x_axis, y=medians, mode='lines', line=dict(color=CHART_COLORS["secondary"], width=3), name='Median'))
    fig_line.add_trace(go.Scatter(x=x_axis, y=contributions, mode='lines', line=dict(color=CHART_COLORS["positive"], width=2, dash='dash'), name='Total contributed'))
    
    fig_line.update_layout(
        title="Projected portfolio value",
        xaxis_title="Years",
        yaxis_title="Value ($)",
        template="plotly_white",
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Grafici inferiori
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        st.markdown("#### Active allocation")
        fig_pie = go.Figure(data=[go.Pie(labels=['Stocks', 'Bonds', 'Cash'], values=[stocks, bonds, cash], hole=.6, marker_colors=[CHART_COLORS["stocks"], CHART_COLORS["bonds"], CHART_COLORS["cash"]])])
        fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with b_col2:
        st.markdown("#### Final-value distribution")
        fig_hist = go.Figure(data=[go.Histogram(y=final_values, orientation='h', marker_color=CHART_COLORS["secondary"], nbinsy=30)])
        fig_hist.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, xaxis_title="Count", yaxis_title="Final Value ($)", template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)

run()

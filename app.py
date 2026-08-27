import streamlit as st
import numpy as np
import plotly.express as px
from model import ModelParameters, SimulationResults, run_avellaneda_model
import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go

def get_slider_params() -> ModelParameters:
    simulations : int = st.sidebar.slider(label="Simulation Count", min_value=1, max_value=1000, value=1000)
    s : float = st.sidebar.slider(label="Inital Price", min_value=0, max_value=100, value=100, on_change=update_seed)
    T : float = st.sidebar.slider(label="Time Horizon", min_value=0.1, max_value=10.0, value=1.0)
    sigma : float = st.sidebar.slider(label="Volatility", min_value=0.1, max_value=10.0, value=1.0)
    N : int = st.sidebar.slider(label="N", min_value=100, max_value=200, value=200)

    init_q : int = st.sidebar.slider(label="Inital Inventory", min_value=0, max_value=2, value=0)
    gamma : float = st.sidebar.slider(label="Gamma", min_value=0.1, max_value=1.0, value=0.1)
    k : float = st.sidebar.slider(label="k", min_value=0.1, max_value=2.0, value=1.5)
    M : float = st.sidebar.slider(label="M", min_value=0.0, max_value=1.0, value=0.5)
    init_cash : float = st.sidebar.slider(label="Cash", min_value=0.0, max_value=100.0, value=0.0)
    return ModelParameters(simulations,s,T,sigma,N,init_q,gamma,k,M,init_cash)

def plot_dashboard(results : SimulationResults, path_idx):
    st.subheader(f"Showing Path {path_idx + 1}")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=results.t, y=results.S[path_idx], mode='lines', name='Mid-Price', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=results.t, y=results.reservations[path_idx], mode='lines', name='Reservation', line=dict(dash='dot', color='orange', width=2)))
    fig.add_trace(go.Scatter(x=results.t, y=results.bid_prices[path_idx], mode='lines', name='Bid Quote', line=dict(color='green', width=1)))
    fig.add_trace(go.Scatter(x=results.t, y=results.ask_prices[path_idx], mode='lines', name='Ask Quote', line=dict(color='red', width=1)))

    bid_mask = results.bid_arrive[path_idx] == 1
    ask_mask = results.ask_arrive[path_idx] == 1

    if bid_mask.any():
        fig.add_trace(go.Scatter(x=results.t[bid_mask], y=results.bid_prices[path_idx][bid_mask], mode='markers', 
                                 name='Bid Filled', marker=dict(color='darkgreen', size=8, symbol='triangle-up')))
        
    if ask_mask.any():
        fig.add_trace(go.Scatter(x=results.t[ask_mask], y=results.ask_prices[path_idx][ask_mask], mode='markers', 
                                 name='Ask Filled', marker=dict(color='darkred', size=8, symbol='triangle-down')))

    fig.update_layout(xaxis_title="Time (t)", yaxis_title="Price", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    
    # distribution
    st.subheader(f"Profit Distribution ({len(results.profits)} Simulations)")
    fig_hist = px.histogram(
        x=results.profits, 
        nbins=50, 
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(xaxis_title="Final Profit", yaxis_title="Count", showlegend=False)
    st.plotly_chart(fig_hist, use_container_width=True)

st.title("Avellaneda-Stoikov market-making model")

if 'seed' not in st.session_state:
    st.session_state.seed = np.random.randint(0, 1000000)
def update_seed():
    st.session_state.seed = np.random.randint(0, 1000000)


params : ModelParameters = get_slider_params()
results : SimulationResults = run_avellaneda_model(params, st.session_state.seed)


st.divider()
st.subheader("Simulation Metrics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Mean Profit", value=f"{np.mean(results.profits):.2f}")
with col2:
    st.metric(label="Std Dev (Profit)", value=f"{np.std(results.profits):.2f}")
with col3:
    st.metric(label="Mean Final Inventory", value=f"{np.mean(results.final_q):.3f}")
with col4:
    st.metric(label="Std Dev (Inventory)", value=f"{np.std(results.final_q):.2f}")


st.divider()
selected_path = st.slider("Select Simulation Path to Visualize", min_value=1, max_value=params.simulations, value=1)
plot_dashboard(results, path_idx=selected_path - 1)








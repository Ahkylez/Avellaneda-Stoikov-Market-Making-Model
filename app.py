import streamlit as st
import numpy as np
import plotly.express as px
from brownian_motion import generate_midprice
import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go

st.title("Market Maker")


if 'seed' not in st.session_state:
    st.session_state.seed = np.random.randint(0, 1000000)
def update_seed():
    st.session_state.seed = np.random.randint(0, 1000000)

@dataclass
class model_parameters:
    simulations : int
    s : float           # Inital Price
    T : float           # Time horizon
    sigma : float       # Volatility
    N : int             # Amount of points in the path
    init_q : int        # Inital Inventory
    gamma : float
    k : float           # Represents the liquidity of the market
    M : float           # Represent Market Spread, ie. the difference between the best bid and ask
    init_cash : float

def get_slider_params() -> model_parameters:
    simulations : int = st.sidebar.slider(label="Simulation Count", min_value=1, max_value=1000)
    s : float = st.sidebar.slider(label="Inital Price", min_value=0, max_value=100, value=100, on_change=update_seed)
    T : float = st.sidebar.slider(label="Time Horizon", min_value=0.1, max_value=10.0, value=1.0)
    sigma : float = st.sidebar.slider(label="Volatility", min_value=0.1, max_value=10.0, value=1.0)
    N : int = st.sidebar.slider(label="N", min_value=100, max_value=200, value=200)

    init_q : int = st.sidebar.slider(label="Inital Inventory", min_value=0, max_value=2, value=0)
    gamma : float = st.sidebar.slider(label="Gamma", min_value=0.1, max_value=1.0, value=0.1)
    k : float = st.sidebar.slider(label="k", min_value=0.1, max_value=2.0, value=1.5)
    M : float = st.sidebar.slider(label="M", min_value=0.0, max_value=1.0, value=0.5)
    init_cash : float = st.sidebar.slider(label="Cash", min_value=0.0, max_value=100.0, value=0.0)
    return model_parameters(simulations,s,T,sigma,N,init_q,gamma,k,M,init_cash)

def run_avellaneda_model(p : model_parameters):
    rng : np.random.Generator = np.random.default_rng(seed=st.session_state.seed)
    var = p.sigma*p.sigma

    dt = p.T/p.N
    # add rng as input instead of seed. More customizable that way.
    S = generate_midprice(dt=dt, initial_price=p.s, volatility=p.sigma, time_horizon=p.T, seed=st.session_state.seed, point_count=p.N, path_count=p.simulations)
    t : np.ndarray = np.linspace(0.0, p.N*dt, p.N)

    reservations = np.empty_like(S)
    bid_prices = np.empty_like(S)
    ask_prices = np.empty_like(S)

    bid_arrive = np.zeros_like(S)
    ask_arrive = np.zeros_like(S)

    profits = np.zeros(p.simulations)
    final_q = np.zeros(p.simulations)
    
    # solving for A
    A = np.exp(-p.k * p.M / 2)

    for path_idx, path in enumerate(S):
        q = p.init_q
        cash = p.init_cash

        for i in range(len(path)):
            reservations[path_idx, i] = path[i] - q * p.gamma * var * (p.T - t[i])

            db = p.gamma * q * var * (p.T - t[i]) + 1/p.gamma * np.log(1 + p.gamma/p.k)
            da = -p.gamma * q * var * (p.T - t[i]) + 1/p.gamma * np.log(1 + p.gamma/p.k)

            bid_prices[path_idx, i] = path[i] - db
            ask_prices[path_idx, i] = path[i] + da

            prob_bid = A * np.exp(-p.k * db)
            prob_ask = A * np.exp(-p.k * da)

            if prob_bid > rng.uniform(0,1):
                bid_arrive[path_idx, i] = 1
                q += 1
                cash -= bid_prices[path_idx, i]
            if prob_ask > rng.uniform(0,1):
                ask_arrive[path_idx, i] = 1
                q -= 1
                cash += ask_prices[path_idx, i]

        profits[path_idx] = cash + q * path[-1]
        final_q[path_idx] = q

    return S, t, reservations, bid_prices, ask_prices, bid_arrive, ask_arrive, profits, final_q


def plot_dashboard(S, t, reservations, bid_prices, ask_prices, bid_arrive, ask_arrive, profits, path_idx):
    st.subheader(f"Showing Path {path_idx + 1}")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=t, y=S[path_idx], mode='lines', name='Mid-Price', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=t, y=reservations[path_idx], mode='lines', name='Reservation', line=dict(dash='dot', color='orange', width=2)))
    fig.add_trace(go.Scatter(x=t, y=bid_prices[path_idx], mode='lines', name='Bid Quote', line=dict(color='green', width=1)))
    fig.add_trace(go.Scatter(x=t, y=ask_prices[path_idx], mode='lines', name='Ask Quote', line=dict(color='red', width=1)))

    bid_mask = bid_arrive[path_idx] == 1
    ask_mask = ask_arrive[path_idx] == 1

    if bid_mask.any():
        fig.add_trace(go.Scatter(x=t[bid_mask], y=bid_prices[path_idx][bid_mask], mode='markers', 
                                 name='Bid Filled', marker=dict(color='darkgreen', size=8, symbol='triangle-up')))
        
    if ask_mask.any():
        fig.add_trace(go.Scatter(x=t[ask_mask], y=ask_prices[path_idx][ask_mask], mode='markers', 
                                 name='Ask Filled', marker=dict(color='darkred', size=8, symbol='triangle-down')))

    fig.update_layout(xaxis_title="Time (t)", yaxis_title="Price", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    
    # distribution
    st.subheader(f"Profit Distribution ({len(profits)} Simulations)")
    fig_hist = px.histogram(
        x=profits, 
        nbins=50, 
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(xaxis_title="Final Profit", yaxis_title="Count", showlegend=False)
    st.plotly_chart(fig_hist, use_container_width=True)


    

params : model_parameters = get_slider_params()
S, t, reservations, bid_prices, ask_prices, bid_arrive, ask_arrive, profits, final_q = run_avellaneda_model(params)


st.divider()
st.subheader("Simulation Metrics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Mean Profit", value=f"{np.mean(profits):.2f}")
with col2:
    st.metric(label="Std Dev (Profit)", value=f"{np.std(profits):.2f}")
with col3:
    st.metric(label="Mean Final Inventory", value=f"{np.mean(final_q):.3f}")
with col4:
    st.metric(label="Std Dev (Inventory)", value=f"{np.std(final_q):.2f}")


st.divider()
selected_path = st.slider("Select Simulation Path to Visualize", min_value=1, max_value=params.simulations, value=1)
plot_dashboard(S, t, reservations, bid_prices, ask_prices, bid_arrive, ask_arrive, profits, path_idx=selected_path - 1)

# fix global st.session_state.seed






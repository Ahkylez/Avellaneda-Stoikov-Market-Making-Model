import streamlit as st
import numpy as np
import plotly.express as px
from brownian_motion import generate_midprice
import pandas as pd
from dataclasses import dataclass


st.title("Market Maker")


if 'seed' not in st.session_state:
    st.session_state.seed = np.random.randint(0, 1000000)
def update_seed():
    st.session_state.seed = np.random.randint(0, 1000000)

@dataclass
class model_parameters:
    simulations : int
    s : float
    T : float
    sigma : float
    N : int
    q : int
    gamma : float
    k : float
    M : float 
    cash : float

def get_slider_params() -> model_parameters:
    simulations : int = st.sidebar.slider(label="Simulation Count", min_value=1, max_value=1000)
    s : float = st.sidebar.slider(label="Inital Price", min_value=0, max_value=100, value=100, on_change=update_seed)
    T : float = st.sidebar.slider(label="Time Horizon", min_value=0.1, max_value=10.0, value=1.0)
    sigma : float = st.sidebar.slider(label="Volatility", min_value=0.1, max_value=10.0, value=1.0)
    N : int = st.sidebar.slider(label="N", min_value=100, max_value=1000, value=1000)

    q : int = st.sidebar.slider(label="Inital Inventory", min_value=0, max_value=2, value=0)
    gamma : float = st.sidebar.slider(label="Gamma", min_value=0.1, max_value=1.0, value=0.1)
    k : float = st.sidebar.slider(label="k", min_value=0.1, max_value=2.0, value=1.5)
    M : float = st.sidebar.slider(label="M", min_value=0.0, max_value=1.0, value=0.5)
    cash : float = st.sidebar.slider(label="Cash", min_value=0.0, max_value=100.0, value=0.0)
    return model_parameters(simulations,s,T,sigma,N,q,gamma,k,M,cash)

def run_avellaneda_model(p : model_parameters):
    var = p.sigma*p.sigma

    dt = p.T/p.N
    S = generate_midprice(dt=dt, initial_price=p.s, volatility=p.sigma, time_horizon=p.T, seed=st.session_state.seed, point_count=p.N, path_count=p.simulations)
    t : np.ndarray = np.linspace(0.0, p.N*dt, p.N)

    reservations = np.empty_like(S)
    bid_prices = np.empty_like(S)
    ask_prices = np.empty_like(S)


    for path_idx, path in enumerate(S):


        for i in range(len(path)):
            reservations[path_idx, i] = path[i] - p.q * p.gamma * var * (p.T - t[i])

            db = p.gamma * p.q * var * (p.T - t[i]) + 1/p.gamma * np.log(1 + p.gamma/p.k)
            da = -p.gamma * p.q * var * (p.T - t[i]) + 1/p.gamma * np.log(1 + p.gamma/p.k)

            bid_prices[path_idx, i] = path[i] - db
            ask_prices[path_idx, i] = path[i] + da



    return S, t, reservations, bid_prices, ask_prices


    # A = np.exp(-k * M/2) / dt
    # rng : np.random.Generator = np.random.default_rng(seed=st.session_state.seed)

    # for path in S:
    #     q = 0
    #     cash = 0
    #     arrival_bid = np.zeros_like(path)
    #     arrival_ask= np.zeros_like(path)

    #     profits = []
    #     final_qs = []

    #     for i in range(len(path)):
    #         r = path - q * gamma * var * (T - t[i])

    #         db = gamma * q * var * (T - t[i]) + 1/gamma * np.log(1 + gamma/k)
    #         da = -gamma * q * var * (T - t[i]) + 1/gamma * np.log(1 + gamma/k)

    #         bid_price = path[i] - db
    #         ask_price = path[i] + da

    #         arrival_bid[i] = A * np.exp(-k * db)
    #         arrival_ask[i] = A * np.exp(-k * da)

    #         p_bid = arrival_bid[i] * dt
    #         p_ask = arrival_ask[i] * dt

    #         if rng.uniform(0, 1) < p_bid:
    #             q += 1
    #             cash -= bid_price

    #         if rng.uniform(0, 1) < p_ask:
    #             q -= 1
    #             cash += ask_price

    #     profit = cash + q * path[-1]  
    #     profits.append(profit)
    #     final_qs.append(q)

def plot_model(S, t, reservations, bid_prices, ask_prices):
    df = pd.DataFrame(S.T, index=t)
    fig = px.line(df, title='Modeled Stock Price', labels={'index': 'Time (t)', 'value': 'Stock Price', 'variable': 'Path'})
    df_res = pd.DataFrame(reservations.T, index=t)
    df_bid = pd.DataFrame(bid_prices.T, index=t)
    df_ask = pd.DataFrame(ask_prices.T, index=t)

    
    
    for col in df_res.columns:
        fig.add_scatter(x=t, y=df_res[col], mode='lines', 
                        name=f'Reservation {col}', 
                        line=dict(dash='dot', width=2))

    for col in df_bid.columns:
        fig.add_scatter(x=t, y=df_bid[col], mode='lines', 
                        name=f'Ask {col}', 
                        line=dict(width=1, color='green'))

    for col in df_ask.columns:
            fig.add_scatter(x=t, y=df_ask[col], mode='lines', 
                            name=f'Ask {col}', 
                            line=dict(width=1, color='red'))
    st.plotly_chart(fig)



params : model_parameters = get_slider_params()
S, t, reservations, bid_prices, ask_prices = run_avellaneda_model(params)
plot_model(S, t, reservations, bid_prices, ask_prices)







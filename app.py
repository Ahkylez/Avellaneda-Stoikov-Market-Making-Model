import streamlit as st
import numpy as np
import plotly.express as px
from brownian_motion import generate_midprice
import pandas as pd


st.title("Market Maker")

# s = 100
# T = 1.0
# sigma = 2
# var = sigma*sigma

# points = 1000
# q = 0
# gamma = 0.1
# k = 1.5
# M = 0.5
# cash = 0

if 'seed' not in st.session_state:
    st.session_state.seed = np.random.randint(0, 1000000)
def update_seed():
    st.session_state.seed = np.random.randint(0, 1000000)

s : float = st.sidebar.slider(label="Inital Price", min_value=0, max_value=100, value=100, on_change=update_seed)
T : float = st.sidebar.slider(label="Time Horizon", min_value=0.1, max_value=10.0, value=1.0)
sigma : float = st.sidebar.slider(label="Volatility", min_value=0.1, max_value=10.0, value=1.0)
points : int = st.sidebar.slider(label="Points", min_value=100, max_value=1000, value=1000)

q : int = st.sidebar.slider(label="Inital Inventory", min_value=0, max_value=2, value=0)
gamma : float = st.sidebar.slider(label="Gamma", min_value=0.1, max_value=1.0, value=0.1)
k : float = st.sidebar.slider(label="k", min_value=0.1, max_value=2.0, value=1.5)
M : float = st.sidebar.slider(label="M", min_value=0.0, max_value=1.0, value=0.5)
cash : float = st.sidebar.slider(label="Volatility", min_value=0.0, max_value=100.0, value=0.0)


S = generate_midprice(initial_price=s, volatility=sigma, time_horizon=T, seed=st.session_state.seed, point_count=1000, path_count=1)
t : np.ndarray = np.linspace(0, T, 1000) # t is duplicated fix this later. 




df = pd.DataFrame(S.T, index=t)


fig = px.line(df, title='Modeled Stock Price', labels={'index': 'Time (t)', 'value': 'Stock Price', 'variable': 'Path'})
st.plotly_chart(fig)




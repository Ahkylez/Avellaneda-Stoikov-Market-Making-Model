import streamlit as st
import numpy as np
import plotly.express as px
from brownian_motion import generate_midprice
import pandas as pd


st.title("Market Maker")

if st.button(label= "Model Stock Prices", type='primary'):
    S = generate_midprice(100, 2, 1.0, point_count=1000, path_count=10)
    t : np.ndarray = np.linspace(0, 1.0, 1000)

    df = pd.DataFrame(S.T, index=t)

    fig = px.line(df, title='Modeled Stock Price', labels={'index': 'Time (t)', 'value': 'Stock Price', 'variable': 'Path'})
    st.plotly_chart(fig)


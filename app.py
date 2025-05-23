import streamlit as st
import pandas as pd
from plot import plot_candlestick
from chatbot import get_bot_response
import os
st.set_page_config(layout='wide', page_title="Stock Dashboard with AI Chat")

df = pd.read_csv("data/stock_data.csv", parse_dates=['timestamp'])

st.write(df.head())
st.write(df.shape)

tab1, tab2 = st.tabs(["📊 Chart", "🤖 AI Chatbot"])

with tab1:
    st.title("Candlestick Chart with Markers and Bands")
    fig = plot_candlestick(df)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.title("Ask AI about Stock Data")
    user_input = st.text_input("Ask me anything about TSLA stock trends...")
    if user_input:
        response = get_bot_response(df, user_input)
        st.write(response)

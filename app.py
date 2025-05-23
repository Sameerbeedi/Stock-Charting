import streamlit as st
import pandas as pd
from plot import plot_candlestick
from chatbot import get_bot_response

st.set_page_config(layout='wide', page_title="Stock Dashboard with AI Chat")

# Load and format stock data
df = pd.read_csv("data/stock_data.csv", parse_dates=["timestamp"])

# If Support/Resistance columns are stored as strings like "[210, 212]", convert them to lists
for col in ["Support", "Resistance"]:
    if col in df.columns and df[col].dtype == object:
        df[col] = df[col].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith("[") else [])

# Tabs for chart and chatbot
tab1, tab2 = st.tabs(["📊 Chart", "🤖 AI Chatbot"])

with tab1:
    st.title("Candlestick Chart with Markers and Bands")
    try:
        plot_candlestick(df)
    except Exception as e:
        st.error(f"Error plotting chart: {e}")

with tab2:
    st.title("Ask AI about Stock Data")
    user_input = st.text_input("Ask me anything about TSLA stock trends...")
    if user_input:
        try:
            response = get_bot_response(df, user_input)
            st.write(response)
        except Exception as e:
            st.error(f"Error from AI chatbot: {e}")

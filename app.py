# app.py
import streamlit as st
import pandas as pd
from plotly.graph_objs import Figure, Candlestick, Scatter, Layout, Shape
import plotly.graph_objs as go
from chatbot import get_bot_response  # defined in chatbot.py
import ast

st.set_page_config(layout='wide', page_title="📈 Stock Dashboard with AI")

@st.cache_data
def load_data():
    df = pd.read_csv("data/stock_data.csv", parse_dates=['timestamp'])

    for col in ["Support", "Resistance"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

    return df

def plot_candlestick(df):
    fig = Figure()

    # Base candlestick
    fig.add_trace(Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candles'
    ))

    # Arrow markers
    long_x, long_y = [], []
    short_x, short_y = [], []
    none_x, none_y = [], []

    for idx, row in df.iterrows():
        if row['direction'] == 'LONG':
            long_x.append(row['timestamp'])
            long_y.append(row['low'] - 2)
        elif row['direction'] == 'SHORT':
            short_x.append(row['timestamp'])
            short_y.append(row['high'] + 2)
        else:
            none_x.append(row['timestamp'])
            none_y.append((row['high'] + row['low']) / 2)

    # Green up arrow
    fig.add_trace(Scatter(
        x=long_x,
        y=long_y,
        mode='markers',
        marker=dict(symbol='arrow-up', color='green', size=15),
        name='LONG'
    ))

    # Red down arrow
    fig.add_trace(Scatter(
        x=short_x,
        y=short_y,
        mode='markers',
        marker=dict(symbol='arrow-down', color='red', size=15),
        name='SHORT'
    ))

    # Yellow dot for None
    fig.add_trace(Scatter(
        x=none_x,
        y=none_y,
        mode='markers',
        marker=dict(symbol='circle', color='yellow', size=10),
        name='No Signal'
    ))

    # Bands
    for _, row in df.iterrows():
        x0 = row['timestamp']
        x1 = row['timestamp']
        if row['Support']:
            fig.add_shape(
                type='rect',
                x0=x0, x1=x1,
                y0=min(row['Support']),
                y1=max(row['Support']),
                line=dict(width=0),
                fillcolor='rgba(0,255,0,0.2)',
                layer='below',
            )
        if row['Resistance']:
            fig.add_shape(
                type='rect',
                x0=x0, x1=x1,
                y0=min(row['Resistance']),
                y1=max(row['Resistance']),
                line=dict(width=0),
                fillcolor='rgba(255,0,0,0.2)',
                layer='below',
            )

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title='Candlestick Chart with Markers and Bands',
        template='plotly_dark',
        height=800
    )

    st.plotly_chart(fig, use_container_width=True)

# Load Data
df = load_data()

if df is not None:
    tab1, tab2 = st.tabs(["📊 Visualization", "🤖 AI Chatbot"])

    with tab1:
        st.title("Stock Visual Analysis")
        plot_candlestick(df)

    with tab2:
        st.title("Ask AI about Stock Trends")
        question = st.text_input("Ask a question about TSLA data (e.g., How many LONG days in 2023?)")
        if question:
            response = get_bot_response(df, question)
            st.write(response)
else:
    st.error("Failed to load data.")

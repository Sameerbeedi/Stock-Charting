# app.py
import streamlit as st
import pandas as pd
from plotly.graph_objs import Figure, Candlestick, Scatter, Layout
import plotly.graph_objs as go
from chatbot import get_bot_response  
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
    print("Starting plot_candlestick")
    fig = Figure()
    print("Figure created")

    # Base candlestick
    fig.add_trace(Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candles'
    ))
    print("Added candlestick trace")

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
    print("Added markers")

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
    print("Added bands")

    # Support and Resistance lines
    if 'Support' in df.columns:
        support_min = [min(x) if isinstance(x, list) and x else None for x in df['Support']]
        support_max = [max(x) if isinstance(x, list) and x else None for x in df['Support']]
        fig.add_traces([
            go.Scatter(
                x=df['timestamp'], y=support_min,
                mode='lines', line=dict(width=0), showlegend=False,
                hoverinfo='skip'
            ),
            go.Scatter(
                x=df['timestamp'], y=support_max,
                mode='lines', fill='tonexty', fillcolor='rgba(0,255,0,0.2)',
                line=dict(width=0), showlegend=True, name='Support Band',
                hoverinfo='skip'
            )
        ])

    if 'Resistance' in df.columns:
        resistance_min = [min(x) if isinstance(x, list) and x else None for x in df['Resistance']]
        resistance_max = [max(x) if isinstance(x, list) and x else None for x in df['Resistance']]
        fig.add_traces([
            go.Scatter(
                x=df['timestamp'], y=resistance_min,
                mode='lines', line=dict(width=0), showlegend=False,
                hoverinfo='skip'
            ),
            go.Scatter(
                x=df['timestamp'], y=resistance_max,
                mode='lines', fill='tonexty', fillcolor='rgba(255,0,0,0.2)',
                line=dict(width=0), showlegend=True, name='Resistance Band',
                hoverinfo='skip'
            )
        ])
    print("Added support and resistance lines")

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title='Candlestick Chart with Markers and Bands',
        template='plotly_dark',
        height=800
    )
    print("Returning figure")

    return fig

# Load Data
df = load_data()

# Limit data to the last 200 entries
#df = df.tail(200)  


print("Loaded data")


if df is not None:
    tab1, tab2 = st.tabs(["📊 Visualization", "🤖 AI Chatbot"])

    with tab1:
        st.title("Stock Visual Analysis")
        try:
            # Only pass the last 200 rows to the plot function
            fig = plot_candlestick(df.tail(200))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error plotting chart: {e}")
            st.write(e)

    with tab2:
        st.title("Ask AI about Stock Trends")
        question = st.text_input("Ask a question about TSLA data (e.g., How many LONG days in 2023?)")
        if question:
            response = get_bot_response(df, question)
            st.write(response)
else:
    st.error("Failed to load data.")

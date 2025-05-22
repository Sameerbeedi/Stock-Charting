import pandas as pd
import plotly.graph_objects as go

def plot_candlestick(df):
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='Candles'))

    # Markers
    for i, row in df.iterrows():
        if row['Direction'] == 'LONG':
            fig.add_trace(go.Scatter(
                x=[row['Date']], y=[row['Low'] - 1],
                mode='markers',
                marker=dict(symbol='arrow-up', color='green', size=15),
                name='LONG'))
        elif row['Direction'] == 'SHORT':
            fig.add_trace(go.Scatter(
                x=[row['Date']], y=[row['High'] + 1],
                mode='markers',
                marker=dict(symbol='arrow-down', color='red', size=15),
                name='SHORT'))
        elif row['Direction'] is None or pd.isna(row['Direction']):
            fig.add_trace(go.Scatter(
                x=[row['Date']], y=[(row['High'] + row['Low']) / 2],
                mode='markers',
                marker=dict(symbol='circle', color='yellow', size=10),
                name='Neutral'))

    # Support bands
    for i, row in df.iterrows():
        if pd.notna(row['Support']):
            support = eval(row['Support'])
            fig.add_shape(type='rect',
                x0=row['Date'], x1=row['Date'],
                y0=min(support), y1=max(support),
                fillcolor='rgba(0,255,0,0.2)', line=dict(width=0))

    # Resistance bands
    for i, row in df.iterrows():
        if pd.notna(row['Resistance']):
            resistance = eval(row['Resistance'])
            fig.add_shape(type='rect',
                x0=row['Date'], x1=row['Date'],
                y0=min(resistance), y1=max(resistance),
                fillcolor='rgba(255,0,0,0.2)', line=dict(width=0))

    fig.update_layout(xaxis_rangeslider_visible=False, height=600)
    return fig

import pandas as pd
import plotly.graph_objects as go

def plot_candlestick(df):
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df['timestamp'], open=df['open'], high=df['high'],
        low=df['low'], close=df['close'], name='Candles'))

    # Markers
    for i, row in df.iterrows():
        if row['direction'] == 'LONG':
            fig.add_trace(go.Scatter(
                x=[row['timestamp']], y=[row['low'] - 1],
                mode='markers',
                marker=dict(symbol='arrow-up', color='green', size=15),
                name='LONG'))
        elif row['direction'] == 'SHORT':
            fig.add_trace(go.Scatter(
                x=[row['timestamp']], y=[row['high'] + 1],
                mode='markers',
                marker=dict(symbol='arrow-down', color='red', size=15),
                name='SHORT'))
        elif row['direction'] is None or pd.isna(row['direction']):
            fig.add_trace(go.Scatter(
                x=[row['timestamp']], y=[(row['high'] + row['low']) / 2],
                mode='markers',
                marker=dict(symbol='circle', color='yellow', size=10),
                name='Neutral'))

    # Support bands
    for i, row in df.iterrows():
        if pd.notna(row['Support']):
            support = eval(row['Support'])
            if support:  
                fig.add_shape(type='rect',
                    x0=row['timestamp'], x1=row['timestamp'],
                    y0=min(support), y1=max(support),
                    fillcolor='rgba(0,255,0,0.2)', line=dict(width=0))

    # Resistance bands
    for i, row in df.iterrows():
        if pd.notna(row['Resistance']):
            resistance = eval(row['Resistance'])
            if resistance:  
                fig.add_shape(type='rect',
                    x0=row['timestamp'], x1=row['timestamp'],
                    y0=min(resistance), y1=max(resistance),
                    fillcolor='rgba(255,0,0,0.2)', line=dict(width=0))

    fig.update_layout(xaxis_rangeslider_visible=False, height=600)
    return fig

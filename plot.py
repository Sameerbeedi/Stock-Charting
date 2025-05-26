import plotly.graph_objects as go
import pandas as pd

def plot_candlestick(df):
    fig = go.Figure()

    # Add candlestick trace
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candlestick',
        increasing_line_color='green',
        decreasing_line_color='red'
    ))

    # Add markers for LONG, SHORT, None
    for i, row in df.iterrows():
        if row['direction'] == 'LONG':
            fig.add_trace(go.Scatter(
                x=[row['timestamp']],
                y=[row['low'] * 0.995],  # Slightly below the candle
                mode='markers',
                marker=dict(symbol='arrow-up', color='green', size=12),
                name='LONG',
                showlegend=False
            ))
        elif row['direction'] == 'SHORT':
            fig.add_trace(go.Scatter(
                x=[row['timestamp']],
                y=[row['high'] * 1.005],  # Slightly above the candle
                mode='markers',
                marker=dict(symbol='arrow-down', color='red', size=12),
                name='SHORT',
                showlegend=False
            ))
        elif pd.isna(row['direction']) or row['direction'] is None:
            fig.add_trace(go.Scatter(
                x=[row['timestamp']],
                y=[(row['high'] + row['low']) / 2],
                mode='markers',
                marker=dict(symbol='circle', color='yellow', size=10),
                name='NEUTRAL',
                showlegend=False
            ))

    # Add support bands (green)
    if 'Support' in df.columns:
        for i, row in df.iterrows():
            if isinstance(row['Support'], list) and row['Support']:
                support_low = min(row['Support'])
                support_high = max(row['Support'])
                fig.add_shape(
                    type="rect",
                    x0=row['timestamp'], x1=row['timestamp'],
                    y0=support_low, y1=support_high,
                    fillcolor="rgba(0,255,0,0.15)",
                    line=dict(width=0),
                    layer="below"
                )

    # Add resistance bands (red)
    if 'Resistance' in df.columns:
        for i, row in df.iterrows():
            if isinstance(row['Resistance'], list) and row['Resistance']:
                resistance_low = min(row['Resistance'])
                resistance_high = max(row['Resistance'])
                fig.add_shape(
                    type="rect",
                    x0=row['timestamp'], x1=row['timestamp'],
                    y0=resistance_low, y1=resistance_high,
                    fillcolor="rgba(255,0,0,0.15)",
                    line=dict(width=0),
                    layer="below"
                )

    fig.update_layout(
        title='TSLA Candlestick Chart with Markers and Bands',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        height=700
    )

    fig.update_xaxes(type='category')  # Helps prevent gaps in date labels

    fig.show()

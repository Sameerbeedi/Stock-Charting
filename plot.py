import plotly.graph_objects as go
import pandas as pd

def plot_candlestick(df):
    print("Start plotting")
    fig = go.Figure()
    print("Figure created")
    print("DF shape in plot:", df.shape)
    print("Columns:", df.columns)

    # Ensure timestamp column is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

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
    print("Added candlestick trace")

    # Group markers by direction for efficiency
    long_x = []
    long_y = []
    short_x = []
    short_y = []
    neutral_x = []
    neutral_y = []

    for i, row in df.iterrows():
        direction = row.get('direction', None)
        if direction == 'LONG':
            long_x.append(row['timestamp'])
            long_y.append(row['low'] * 0.995)  # Slightly below candle
        elif direction == 'SHORT':
            short_x.append(row['timestamp'])
            short_y.append(row['high'] * 1.005)  # Slightly above candle
        else:
            # Treat any other or NaN as neutral
            neutral_x.append(row['timestamp'])
            neutral_y.append((row['high'] + row['low']) / 2)

    # Add LONG markers
    if long_x:
        fig.add_trace(go.Scatter(
            x=long_x,
            y=long_y,
            mode='markers',
            marker=dict(symbol='arrow-up', color='green', size=12),
            name='LONG'
        ))

    # Add SHORT markers
    if short_x:
        fig.add_trace(go.Scatter(
            x=short_x,
            y=short_y,
            mode='markers',
            marker=dict(symbol='arrow-down', color='red', size=12),
            name='SHORT'
        ))

    # Add NEUTRAL markers
    if neutral_x:
        fig.add_trace(go.Scatter(
            x=neutral_x,
            y=neutral_y,
            mode='markers',
            marker=dict(symbol='circle', color='yellow', size=10),
            name='NEUTRAL'
        ))
    print("Added markers")

    # Add support bands (green rectangles)
    if 'Support' in df.columns:
        for i, row in df.iterrows():
            supports = row['Support']
            if isinstance(supports, list) and supports:
                support_low = min(supports)
                support_high = max(supports)
                ts = row['timestamp']
                fig.add_shape(
                    type="rect",
                    xref="x",
                    yref="y",
                    x0=ts - pd.Timedelta(minutes=30),
                    x1=ts + pd.Timedelta(minutes=30),
                    y0=support_low,
                    y1=support_high,
                    fillcolor="rgba(0,255,0,0.15)",
                    line=dict(width=0),
                    layer="below"
                )

    # Add resistance bands (red rectangles)
    if 'Resistance' in df.columns:
        for i, row in df.iterrows():
            resistances = row['Resistance']
            if isinstance(resistances, list) and resistances:
                resistance_low = min(resistances)
                resistance_high = max(resistances)
                ts = row['timestamp']
                fig.add_shape(
                    type="rect",
                    xref="x",
                    yref="y",
                    x0=ts - pd.Timedelta(minutes=30),
                    x1=ts + pd.Timedelta(minutes=30),
                    y0=resistance_low,
                    y1=resistance_high,
                    fillcolor="rgba(255,0,0,0.15)",
                    line=dict(width=0),
                    layer="below"
                )
    print("Added bands")

    fig.update_layout(
        title='TSLA Candlestick Chart with Markers and Bands',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        height=700
    )

    # Use date type for x-axis for proper datetime handling
    fig.update_xaxes(type='date')

    print("Returning figure")
    return fig

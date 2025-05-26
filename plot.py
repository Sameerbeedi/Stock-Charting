import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_candlestick(df):
    """
    Alternative implementation using Plotly instead of streamlit_lightweight_charts
    This should be more reliable for complex data structures
    """
    df = df.copy()
    df = df.sort_values('timestamp')
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.8, 0.2],
        subplot_titles=('Price Chart', 'Volume')
    )
    
    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name="OHLC"
        ),
        row=1, col=1
    )
    
    # Add volume if available
    if 'volume' in df.columns:
        fig.add_trace(
            go.Bar(
                x=df['timestamp'],
                y=df['volume'],
                name="Volume",
                marker_color='rgba(158,202,225,0.8)',
            ),
            row=2, col=1
        )
    
    # Add support and resistance levels
    for _, row in df.iterrows():
        timestamp = row['timestamp']
        
        # Add support levels
        support_data = row.get('Support', [])
        if isinstance(support_data, list) and len(support_data) > 0:
            for level in support_data:
                try:
                    level = float(level)
                    fig.add_hline(
                        y=level,
                        line_dash="dash",
                        line_color="green",
                        line_width=1,
                        opacity=0.6,
                        row=1
                    )
                except (ValueError, TypeError):
                    continue
        
        # Add resistance levels
        resistance_data = row.get('Resistance', [])
        if isinstance(resistance_data, list) and len(resistance_data) > 0:
            for level in resistance_data:
                try:
                    level = float(level)
                    fig.add_hline(
                        y=level,
                        line_dash="dash",
                        line_color="red",
                        line_width=1,
                        opacity=0.6,
                        row=1
                    )
                except (ValueError, TypeError):
                    continue
    
    # Add direction markers
    long_dates = []
    long_prices = []
    short_dates = []
    short_prices = []
    
    for _, row in df.iterrows():
        direction = row.get('direction', None)
        if direction == 'LONG':
            long_dates.append(row['timestamp'])
            long_prices.append(row['low'] * 0.995)  # Slightly below the low
        elif direction == 'SHORT':
            short_dates.append(row['timestamp'])
            short_prices.append(row['high'] * 1.005)  # Slightly above the high
    
    # Add LONG markers
    if long_dates:
        fig.add_trace(
            go.Scatter(
                x=long_dates,
                y=long_prices,
                mode='markers',
                marker=dict(
                    symbol='triangle-up',
                    size=10,
                    color='green'
                ),
                name='LONG',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Add SHORT markers
    if short_dates:
        fig.add_trace(
            go.Scatter(
                x=short_dates,
                y=short_prices,
                mode='markers',
                marker=dict(
                    symbol='triangle-down',
                    size=10,
                    color='red'
                ),
                name='SHORT',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Update layout
    fig.update_layout(
        title="Candlestick Chart with Markers and Bands",
        xaxis_title="Date",
        yaxis_title="Price",
        height=700,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
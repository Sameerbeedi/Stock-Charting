import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

def plot_candlestick(df):
    df = df.copy()
    df = df.sort_values('timestamp')

    # Prepare the candlestick data
    candles = []
    markers = []
    support_zones = []
    resistance_zones = []

    for _, row in df.iterrows():
        ts = row['timestamp']
        candles.append({
            "time": ts,
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"]
        })

        # Marker logic
        direction = row.get('direction', None)
        if direction == 'LONG':
            markers.append({
                "time": ts,
                "position": "belowBar",
                "color": "green",
                "shape": "arrowUp",
                "text": "LONG"
            })
        elif direction == 'SHORT':
            markers.append({
                "time": ts,
                "position": "aboveBar",
                "color": "red",
                "shape": "arrowDown",
                "text": "SHORT"
            })
        else:
            markers.append({
                "time": ts,
                "position": "inBar",
                "color": "yellow",
                "shape": "circle",
                "text": "N/A"
            })

        # Support band (drawn as separate line series per row range)
        if isinstance(row.get('Support'), list) and len(row['Support']) > 0:
            support_zones.append({
                "time": ts,
                "value": min(row['Support']),
                "color": "rgba(0, 255, 0, 0.3)"
            })
            support_zones.append({
                "time": ts,
                "value": max(row['Support']),
                "color": "rgba(0, 255, 0, 0.3)"
            })

        # Resistance band
        if isinstance(row.get('Resistance'), list) and len(row['Resistance']) > 0:
            resistance_zones.append({
                "time": ts,
                "value": min(row['Resistance']),
                "color": "rgba(255, 0, 0, 0.3)"
            })
            resistance_zones.append({
                "time": ts,
                "value": max(row['Resistance']),
                "color": "rgba(255, 0, 0, 0.3)"
            })

    # Create the series list
    series = [
        {
            "type": "candlestick",
            "data": candles,
            "markers": markers,
        },
        {
            "type": "line",
            "data": support_zones,
            "color": "rgba(0, 255, 0, 0.3)",
            "lineWidth": 1,
        },
        {
            "type": "line",
            "data": resistance_zones,
            "color": "rgba(255, 0, 0, 0.3)",
            "lineWidth": 1,
        }
    ]

    chart_options = {
        "layout": {
            "backgroundColor": "#000000",
            "textColor": "#FFFFFF"
        },
        "priceScale": {
            "borderColor": "#cccccc"
        },
        "timeScale": {
            "borderColor": "#cccccc"
        },
        "crosshair": {
            "mode": 1
        },
        "grid": {
            "vertLines": {"color": "#404040"},
            "horzLines": {"color": "#404040"}
        },
        "width": 1000,
        "height": 500,
    }

    renderLightweightCharts(series, chart_options)


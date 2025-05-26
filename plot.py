import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import json

def plot_candlestick(df):
    df = df.copy()
    df = df.sort_values('timestamp')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    # Prepare the candlestick data
    candles = []
    markers = []
    support_lines = []
    resistance_lines = []

    for _, row in df.iterrows():
        ts = row['timestamp']
        
        # Ensure all values are native Python types, not numpy types
        candles.append({
            "time": ts,
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"])
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

        # Support levels - create individual data points for each level
        support_data = row.get('Support', [])
        if isinstance(support_data, list) and len(support_data) > 0:
            for level in support_data:
                try:
                    support_lines.append({
                        "time": ts,
                        "value": float(level)  # Ensure it's a float, not numpy type
                    })
                except (ValueError, TypeError):
                    continue

        # Resistance levels - create individual data points for each level
        resistance_data = row.get('Resistance', [])
        if isinstance(resistance_data, list) and len(resistance_data) > 0:
            for level in resistance_data:
                try:
                    resistance_lines.append({
                        "time": ts,
                        "value": float(level)  # Ensure it's a float, not numpy type
                    })
                except (ValueError, TypeError):
                    continue

    # Create the series list - only include series that have data
    series = [
        {
            "type": "candlestick",
            "data": candles,
            "markers": markers,
        }
    ]

    # Only add support line if we have support data
    if support_lines:
        series.append({
            "type": "line",
            "data": support_lines,
            "color": "rgba(0, 255, 0, 0.6)",
            "lineWidth": 2,
            "lineStyle": 2,  # Dashed line
            "title": "Support"
        })

    # Only add resistance line if we have resistance data
    if resistance_lines:
        series.append({
            "type": "line",
            "data": resistance_lines,
            "color": "rgba(255, 0, 0, 0.6)",
            "lineWidth": 2,
            "lineStyle": 2,  # Dashed line
            "title": "Resistance"
        })

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

    try:
        # Ensure all data is JSON serializable
        def make_serializable(obj):
            """Convert numpy types and other non-serializable types to basic Python types"""
            if hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif hasattr(obj, 'tolist'):  # numpy array
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            else:
                return obj
        
        # Clean the data
        clean_series = make_serializable(series)
        clean_options = make_serializable(chart_options)
        
        # Test JSON serialization to catch any remaining issues
        try:
            json.dumps(clean_series)
            json.dumps(clean_options)
        except TypeError as json_error:
            st.error(f"JSON serialization error: {json_error}")
            return
        
        renderLightweightCharts(clean_series, clean_options)
    except Exception as e:
        st.error(f"Error rendering chart: {e}")
        st.write("Debug info:")
        st.write(f"Number of candles: {len(candles)}")
        st.write(f"Number of support points: {len(support_lines)}")
        st.write(f"Number of resistance points: {len(resistance_lines)}")
        st.write("Sample candle data:", candles[:2] if candles else "No candles")
        st.write("Sample support data:", support_lines[:2] if support_lines else "No support data")
        st.write("Sample resistance data:", resistance_lines[:2] if resistance_lines else "No resistance data")
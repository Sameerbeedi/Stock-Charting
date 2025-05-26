import pandas as pd
import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import json

def plot_candlestick(df):
    """Ultra-minimal implementation to avoid encoding issues"""
    
    # Create a minimal copy with only essential data
    df_clean = df.copy().sort_values('timestamp')
    
    # Convert timestamp to string format
    df_clean['time_str'] = df_clean['timestamp'].dt.strftime('%Y-%m-%d')
    
    # Build data structures using only basic Python types
    candles = []
    markers = []
    
    for idx, row in df_clean.iterrows():
        # Build candle data with explicit type conversion
        candle = {
            "time": str(row['time_str']),
            "open": round(float(row['open']), 3),
            "high": round(float(row['high']), 3),
            "low": round(float(row['low']), 3),
            "close": round(float(row['close']), 3)
        }
        candles.append(candle)
        
        # Add direction markers
        direction = str(row.get('direction', 'NONE'))
        if direction == 'LONG':
            marker = {
                "time": str(row['time_str']),
                "position": "belowBar",
                "color": "#00FF00",
                "shape": "arrowUp",
                "text": "LONG"
            }
            markers.append(marker)
        elif direction == 'SHORT':
            marker = {
                "time": str(row['time_str']),
                "position": "aboveBar", 
                "color": "#FF0000",
                "shape": "arrowDown",
                "text": "SHORT"
            }
            markers.append(marker)
    
    # Create the simplest possible series structure
    series_data = [
        {
            "type": "candlestick",
            "data": candles,
            "markers": markers
        }
    ]
    
    # Minimal chart options
    options = {
        "layout": {
            "backgroundColor": "#000000",
            "textColor": "#FFFFFF"
        },
        "width": 1000,
        "height": 500
    }
    
    # Debug: Print the exact data being sent
    st.write("Sending to chart library:")
    st.write(f"Series type: {type(series_data)}")
    st.write(f"Options type: {type(options)}")
    
    # Test JSON serialization first
    try:
        test_json = json.dumps(series_data, indent=2)
        st.text("JSON serialization test passed")
        
        # Try the actual rendering
        renderLightweightCharts(series_data, options)
        
    except Exception as e:
        st.error(f"Failed: {e}")
        st.code(f"Error type: {type(e)}")
        
        # Show exactly what we're trying to serialize
        st.write("Raw data sample:")
        st.json(series_data[0] if series_data else {})


def plot_candlestick_stepwise(df):
    """Step-by-step debugging version"""
    st.write("=== STEP BY STEP DEBUG ===")
    
    # Step 1: Basic candlestick only
    df_clean = df.copy().sort_values('timestamp').head(10)  # Only 10 rows for testing
    df_clean['time_str'] = df_clean['timestamp'].dt.strftime('%Y-%m-%d')
    
    st.write("Step 1: Creating basic candles...")
    candles = []
    for _, row in df_clean.iterrows():
        candle = {
            "time": str(row['time_str']),
            "open": float(row['open']),
            "high": float(row['high']),
            "low": float(row['low']),
            "close": float(row['close'])
        }
        candles.append(candle)
    
    st.write(f"Created {len(candles)} candles")
    
    # Test 1: Just candles, no markers
    try:
        st.write("Test 1: Basic candlesticks only")
        series1 = [{"type": "candlestick", "data": candles}]
        options1 = {"width": 800, "height": 400}
        
        json.dumps(series1)  # Test serialization
        renderLightweightCharts(series1, options1)
        st.success("✅ Basic candlesticks work!")
        
        return  # If this works, we know the basic setup is fine
        
    except Exception as e:
        st.error(f"❌ Basic candlesticks failed: {e}")
        st.json(candles[0] if candles else {})
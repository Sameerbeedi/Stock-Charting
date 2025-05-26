import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd
import json

# Sample data (can be replaced with your own)
data = pd.DataFrame({
    "time": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05"],
    "open": [100, 105, 110, 108, 112],
    "high": [110, 115, 118, 112, 120],
    "low": [95, 100, 108, 106, 111],
    "close": [108, 112, 110, 111, 118]
})

# Prepare the data in the format required by renderLightweightCharts
series_data = [{
    "type": "candlestick",
    "data": data.to_dict(orient="records")  # Converts each row into a dictionary
}]

# Optional chart options (customize as needed)
options = {
    "width": 800,
    "height": 400,
    "layout": {
        "background": {"color": "#ffffff"},
        "textColor": "#000000"
    },
    "grid": {
        "vertLines": {"color": "#eee"},
        "horzLines": {"color": "#eee"}
    },
    "priceScale": {"position": "right"},
    "timeScale": {"timeVisible": True}
}

# Render chart with proper JSON serialization
renderLightweightCharts(
    json.dumps(series_data),
    json.dumps(options)
)

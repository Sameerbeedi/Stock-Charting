import streamlit as st
import pandas as pd
from streamlit_lightweight_charts import renderLightweightCharts
from chatbot import get_bot_response
import ast
import json

st.set_page_config(layout='wide', page_title="Stock Dashboard with AI Chat")

@st.cache_data
def load_and_process_data():
    """Load and process stock data with proper error handling"""
    try:
        df = pd.read_csv("data/stock_data.csv", parse_dates=["timestamp"])

        for col in ["Support", "Resistance"]:
            if col in df.columns:
                processed_values = []
                for idx, value in enumerate(df[col]):
                    try:
                        if pd.isna(value) or value == '' or value is None:
                            processed_values.append([])
                        elif isinstance(value, str):
                            if value.strip().startswith('[') and value.strip().endswith(']'):
                                processed_values.append(ast.literal_eval(value.strip()))
                            else:
                                try:
                                    nums = [float(x.strip()) for x in value.split(',') if x.strip()]
                                    processed_values.append(nums)
                                except ValueError:
                                    processed_values.append([])
                        elif isinstance(value, (list, tuple)):
                            processed_values.append(list(value))
                        else:
                            try:
                                processed_values.append([float(value)])
                            except (ValueError, TypeError):
                                processed_values.append([])
                    except Exception as e:
                        st.warning(f"Error processing {col} at row {idx}: {e}")
                        processed_values.append([])
                df[col] = processed_values
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def plot_lightweight_candlestick(df):
    try:
        chart_data = df.rename(columns={
            'timestamp': 'time',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close'
        })

        # Convert datetime to ISO format
        chart_data['time'] = chart_data['time'].dt.strftime('%Y-%m-%d')

        candlestick_series = [{
            "type": "candlestick",
            "data": chart_data[['time', 'open', 'high', 'low', 'close']].to_dict(orient="records")
        }]

        chart_options = {
            "width": 800,
            "height": 400,
            "layout": {
                "background": {"color": "#ffffff"},
                "textColor": "#000"
            },
            "grid": {
                "vertLines": {"color": "#eee"},
                "horzLines": {"color": "#eee"}
            },
            "priceScale": {"position": "right"},
            "timeScale": {"timeVisible": True}
        }

        renderLightweightCharts(json.dumps(candlestick_series), json.dumps(chart_options))
    except Exception as e:
        st.error(f"Error rendering lightweight chart: {e}")

# Load data
df = load_and_process_data()

if df is not None:
    tab1, tab2 = st.tabs(["📊 Chart", "🤖 AI Chatbot"])

    with tab1:
        st.title("Candlestick Chart with Lightweight Charts")

        with st.expander("Data Debug Info"):
            st.write("DataFrame shape:", df.shape)
            st.write("Columns:", df.columns.tolist())
            if "Support" in df.columns:
                st.write("Sample Support values:", df["Support"].head().tolist())
            if "Resistance" in df.columns:
                st.write("Sample Resistance values:", df["Resistance"].head().tolist())
            st.write("Data types:")
            st.write(df.dtypes)

        try:
            plot_lightweight_candlestick(df)
        except Exception as e:
            st.error(f"Error plotting chart: {e}")
            st.write("DataFrame info:")
            st.dataframe(df.head())

    with tab2:
        st.title("Ask AI about Stock Data")
        user_input = st.text_input("Ask me anything about TSLA stock trends...")
        if user_input:
            try:
                response = get_bot_response(df, user_input)
                st.write(response)
            except Exception as e:
                st.error(f"Error from AI chatbot: {e}")
else:
    st.error("Failed to load data. Please check your CSV file.")

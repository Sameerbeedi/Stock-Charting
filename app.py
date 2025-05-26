import streamlit as st
import pandas as pd
from plot import plot_candlestick
from chatbot import get_bot_response
import ast

st.set_page_config(layout='wide', page_title="Stock Dashboard with AI Chat")

@st.cache_data
def load_and_process_data():
    """Load and process stock data with proper error handling"""
    try:
        df = pd.read_csv("data/stock_data.csv", parse_dates=["timestamp"])
        
        # Process Support/Resistance columns more safely
        for col in ["Support", "Resistance"]:
            if col in df.columns:
                processed_values = []
                for idx, value in enumerate(df[col]):
                    try:
                        if pd.isna(value) or value == '' or value is None:
                            processed_values.append([])
                        elif isinstance(value, str):
                            if value.strip().startswith('[') and value.strip().endswith(']'):
                                # Use ast.literal_eval instead of eval for safety
                                processed_values.append(ast.literal_eval(value.strip()))
                            else:
                                # Handle comma-separated values
                                try:
                                    nums = [float(x.strip()) for x in value.split(',') if x.strip()]
                                    processed_values.append(nums)
                                except ValueError:
                                    processed_values.append([])
                        elif isinstance(value, (list, tuple)):
                            processed_values.append(list(value))
                        else:
                            # Single number
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

# Load data
df = load_and_process_data()

if df is not None:
    # Tabs for chart and chatbot
    tab1, tab2 = st.tabs(["📊 Chart", "🤖 AI Chatbot"])

    with tab1:
        st.title("Candlestick Chart with Markers and Bands")
        
        # Add data inspection section for debugging
        with st.expander("Data Debug Info"):
            st.write("DataFrame shape:", df.shape)
            st.write("Columns:", df.columns.tolist())
            
            # Show sample of Support/Resistance data
            if "Support" in df.columns:
                st.write("Sample Support values:")
                st.write(df["Support"].head().tolist())
            if "Resistance" in df.columns:
                st.write("Sample Resistance values:")
                st.write(df["Resistance"].head().tolist())
            
            # Show data types
            st.write("Data types:")
            st.write(df.dtypes)
        
        try:
            plot_candlestick(df)
        except Exception as e:
            st.error(f"Error plotting chart: {e}")
            st.write("DataFrame info for debugging:")
            st.write(df.info())
            
            # Show problematic data
            st.write("First few rows of data:")
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
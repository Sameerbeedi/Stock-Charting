import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def get_bot_response(df, query):
    # Extract TSLA related stats
    if "bullish" in query.lower():
        bullish_days = df[df['direction'] == 'LONG'].shape[0]
        return f"TSLA was bullish on {bullish_days} days in the dataset."
    
    elif "support" in query.lower():
        avg_support = df['Support'].dropna().apply(lambda x: sum(eval(x))/len(eval(x)))
        return f"Average support level: {round(avg_support.mean(), 2)}"

    # General fallback using LLM
    response = model.generate_content(
        f"Given this stock dataframe: {df.head(10).to_string()} \nAnswer this: {query}")
    return response.text

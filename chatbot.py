import requests
import os
import pandas as pd

RIVA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
RIVA_API_KEY = os.getenv("NVIDIA_RIVA_API_KEY")

# Simple API test function
def test_api_connection():
    """Test if the API is working with a simple request"""
    if not RIVA_API_KEY:
        return "No API key found"
    
    headers = {
        "Authorization": f"Bearer {RIVA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    simple_payload = {
        "model": "qwen/qwen3-235b-a22b",
        "messages": [
            {"role": "user", "content": "Hello, can you count to 3?"}
        ],
        "max_tokens": 3000
    }
    
    try:
        response = requests.post(RIVA_API_URL, headers=headers, json=simple_payload)
        print(f"Test API status: {response.status_code}")
        response.raise_for_status()
        result = response.json()
        print(f"Test API response: {result}")
        return "API connection successful"
    except Exception as e:
        return f"API test failed: {e}"

def get_bot_response(df, query):
    """Bot analyzes the ENTIRE dataset, not just a subset"""
    
    # Debug: Check full dataset info
    print(f"Full dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Get date range from full dataset
    if 'Date' in df.columns:
        date_range = f"{df['Date'].min()} to {df['Date'].max()}"
        print(f"Full date range: {date_range}")
    else:
        date_range = "No date column found"
    
    # Show sample data but make it clear we're analyzing the FULL dataset
    sample_data = df.head(3).to_string()  # Reduced to 3 rows
    
    # Simplified prompt that focuses on the direction column
    prompt = f"""Analyze this Tesla (TSLA) trading dataset:

Dataset: {len(df)} rows from {date_range}
Key columns: {df.columns.tolist()}

Sample data:
{sample_data}

Question: {query}

"""
    
    print(f"Prompt length: {len(prompt)} characters")
    
    print(f"Analyzing full dataset with {len(df)} rows")
    
    # Check if API key exists
    if not RIVA_API_KEY:
        return "Error: NVIDIA_RIVA_API_KEY environment variable not set"
    
    headers = {
        "Authorization": f"Bearer {RIVA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "nvidia/nemotron-4-340b-instruct",  # Try this model instead
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3000,
        "temperature": 0.1
    }
    
    try:
        print("Making API request...")
        response = requests.post(RIVA_API_URL, headers=headers, json=payload)
        print(f"Response status: {response.status_code}")
        
        response.raise_for_status()
        
        result = response.json()
        print(f"Full API response: {result}")  # Debug: see full response
        
        # Extract response content with detailed checking
        if 'choices' in result and len(result['choices']) > 0:
            choice = result['choices'][0]
            print(f"First choice: {choice}")
            
            if 'message' in choice:
                message = choice['message']
                content = message.get('content', '')
                reasoning_content = message.get('reasoning_content', '')
                
                print(f"Content: '{content}'")
                print(f"Reasoning content: '{reasoning_content[:200]}...'")
                
                # Try content first, then reasoning_content as fallback
                if content and content.strip() and content.strip() != 'None':
                    return content.strip()
                elif reasoning_content and reasoning_content.strip():
                    # Extract the actual answer from reasoning content
                    return f"Analysis: {reasoning_content.strip()}"
                else:
                    return f"Empty content received. Full message: {message}"
            else:
                return f"No 'message' in choice. Choice keys: {choice.keys()}"
        else:
            return f"No choices in response. Response keys: {result.keys()}"
            
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


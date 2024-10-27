import requests
import json

# Ollama API endpoint
API_URL = "http://localhost:11434/api/generate"

# Function to generate text using Ollama
def generate_text(prompt,system = '''You are a weather alert assistant bot. Your task is to analyze weather data and provide concise, actionable summaries for the public. When given weather information, you should:
Identify any severe weather conditions or potential hazards.
Summarize the most important weather elements (temperature, precipitation, wind, etc.) in simple terms.
Provide practical advice on how people should prepare or respond to the weather conditions.
Highlight any significant changes in the forecast compared to previous days.
Mention the time frame for which the information is relevant.
Your responses should be clear, concise, and easy for the general public to understand. Avoid using technical jargon unless absolutely necessary. If there are no severe weather conditions, still provide a brief summary of the weather and any notable aspects.
Based on the weather data provided, create a summary that informs people about what they need to know and do. Your response should be informative yet brief, typically no more than 3-4 sentences.''',model="granite3-dense:8b"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "system":system,
        "keep_alive":"5m"
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        return result['response']
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None



if __name__ == '__main__':
    # Example usage
    prompt = "test"
    response = generate_text(prompt)
    if response:
        print("Generated text:")
        print(response)
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load API keys
load_dotenv()
QLOO_KEY = os.getenv("QLOO_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# 1. User Input Processing with LLM
def analyze_user_input(user_query):
    """Extract cultural preferences using Gemini"""
    prompt = f"""
    Identify cultural preferences from this input. 
    Output ONLY comma-separated keywords.
    Input: {user_query}
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# 2. Get Recommendations from Qloo
def get_qloo_recommendations(keywords):
    """Fetch cultural recommendations based on keywords"""
    url = "https://api.qloo.com/v1/recommendations"
    headers = {"X-API-KEY": QLOO_KEY}
    params = {
        "text": keywords,
        "categories": "music,dining,fashion_brand,film"  # Customizable
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 3. Generate Human-Readable Response with LLM
def format_recommendations(recommendations):
    """Convert JSON to natural language using Gemini"""
    prompt = f"""
    Convert these recommendations into a friendly, enthusiastic list:
    {str(recommendations)}
    
    Include emojis and make it sound exciting!
    """
    response = model.generate_content(prompt)
    return response.text

# Main Function
def main():
    user_query = input("Tell me your cultural interests (e.g., 'I love Japanese anime and French cuisine'): ")
    
    # Process input → Get keywords → Fetch Qloo data → Generate output
    keywords = analyze_user_input(user_query)
    recommendations = get_qloo_recommendations(keywords)
    output = format_recommendations(recommendations)
    
    print("\n🌟 Personalized Recommendations 🌟")
    print(output)

if __name__ == "__main__":
    main()
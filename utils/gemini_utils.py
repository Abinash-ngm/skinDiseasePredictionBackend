import requests
from config import Config
import json

def chat_with_gemini(message, conversation_history=None):
    """
    Send message to Gemini 2.0 Flash API and get health advice
    """
    try:
        api_key = Config.GEMINI_API_KEY
        
        if not api_key:
            raise Exception("Gemini API key not configured")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        # System prompt for health assistant
        system_context = """You are a helpful AI health assistant. Provide accurate, helpful health information while always reminding users to consult healthcare professionals for serious concerns. 
        
Be empathetic, professional, and clear in your responses. If asked about serious symptoms, always recommend seeing a doctor. You can provide general health information, wellness tips, and answer common health questions."""
        
        # Construct conversation
        full_prompt = f"{system_context}\n\nUser question: {message}"
        
        if conversation_history:
            full_prompt = f"{system_context}\n\n{conversation_history}\n\nUser: {message}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        # Extract response text
        if 'candidates' in result and len(result['candidates']) > 0:
            response_text = result['candidates'][0]['content']['parts'][0]['text']
            return response_text
        else:
            return "I'm sorry, I couldn't generate a response. Please try again."
            
    except requests.exceptions.RequestException as e:
        print(f"Gemini API request error: {e}")
        raise Exception(f"Failed to get chatbot response: {str(e)}")
    except Exception as e:
        print(f"Gemini chat error: {e}")
        raise Exception(f"Chat failed: {str(e)}")

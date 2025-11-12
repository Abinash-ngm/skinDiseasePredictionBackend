import requests
from config import Config
import json

def analyze_disease(image_url, disease_type):
    """
    Call Groq API for disease detection
    disease_type: 'skin' or 'eye'
    """
    try:
        api_key = Config.GROQ_API_KEY
        
        if not api_key:
            raise Exception("Groq API key not configured")
        
        # Groq API endpoint for vision/analysis
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Construct prompt based on disease type
        if disease_type == 'skin':
            prompt = f"""Analyze this skin image and detect any potential skin diseases or conditions.
            
Image URL: {image_url}

Provide a response in the following JSON format:
{{
    "disease_name": "Name of the detected condition",
    "confidence": 0.85,
    "severity": "low/medium/high",
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],
    "description": "Brief description of the condition"
}}

Be professional, accurate, and always recommend consulting a dermatologist for proper diagnosis."""
        else:  # eye
            prompt = f"""Analyze this eye image and detect any potential eye diseases or conditions.

Image URL: {image_url}

Provide a response in the following JSON format:
{{
    "disease_name": "Name of the detected condition",
    "confidence": 0.85,
    "severity": "low/medium/high",
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],
    "description": "Brief description of the condition"
}}

Be professional, accurate, and always recommend consulting an ophthalmologist for proper diagnosis."""
        
        payload = {
            "model": "llama-3.2-90b-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        # Try to parse JSON from response
        try:
            # Extract JSON from markdown code blocks if present
            if '```json' in ai_response:
                json_str = ai_response.split('```json')[1].split('```')[0].strip()
            elif '```' in ai_response:
                json_str = ai_response.split('```')[1].split('```')[0].strip()
            else:
                json_str = ai_response.strip()
            
            parsed_result = json.loads(json_str)
            return parsed_result
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "disease_name": "Analysis Completed",
                "confidence": 0.70,
                "severity": "medium",
                "recommendations": [
                    "Consult a medical professional for accurate diagnosis",
                    "Monitor the condition for any changes",
                    "Maintain good hygiene practices"
                ],
                "description": ai_response[:200]
            }
            
    except requests.exceptions.RequestException as e:
        print(f"Groq API request error: {e}")
        raise Exception(f"Failed to analyze image: {str(e)}")
    except Exception as e:
        print(f"Groq analysis error: {e}")
        raise Exception(f"Analysis failed: {str(e)}")

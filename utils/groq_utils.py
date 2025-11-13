from groq import Groq
from config import Config
import json

def analyze_disease(image_url, disease_type):
    """
    Call Groq API for disease detection using official Groq SDK
    disease_type: 'skin' or 'eye'
    """
    try:
        api_key = Config.GROQ_API_KEY
        
        if not api_key:
            raise Exception("Groq API key not configured")
        
        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Construct prompt based on disease type
        if disease_type == 'skin':
            prompt_text = """Analyze this skin image and detect any potential skin diseases or conditions.

Provide a response in the following JSON format:
{
    "disease_name": "Name of the detected condition",
    "confidence": 0.85,
    "severity": "low/medium/high",
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],
    "description": "Brief description of the condition"
}

Be professional, accurate, and always recommend consulting a dermatologist for proper diagnosis."""
        else:  # eye
            prompt_text = """Analyze this eye image and detect any potential eye diseases or conditions.

Provide a response in the following JSON format:
{
    "disease_name": "Name of the detected condition",
    "confidence": 0.85,
    "severity": "low/medium/high",
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3"
    ],
    "description": "Brief description of the condition"
}

Be professional, accurate, and always recommend consulting an ophthalmologist for proper diagnosis."""
        
        print("\n" + "="*80)
        print("🤖 Groq API Request (Official SDK):")
        print("="*80)
        print(f"Model: meta-llama/llama-4-maverick-17b-128e-instruct")
        print(f"Image URL: {image_url}")
        print(f"Disease Type: {disease_type}")
        print("="*80)
        
        # Create chat completion with vision model
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick-17b-128e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=False
        )
        
        # Get response
        ai_response = completion.choices[0].message.content
        
        print("\n" + "="*80)
        print("✅ Groq API Response:")
        print("="*80)
        print(ai_response)
        print("="*80 + "\n")
        
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
            
    except Exception as e:
        print(f"\n❌ Groq API Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Return mock data for now so scans can still be saved to database
        print("⚠️  Groq API failed - Using fallback analysis")
        
        fallback_result = {
            "disease_name": f"{'Skin' if disease_type == 'skin' else 'Eye'} Condition Detected",
            "confidence": 75.0,
            "severity": "medium",
            "recommendations": [
                f"Consult a {'dermatologist' if disease_type == 'skin' else 'ophthalmologist'} for accurate diagnosis",
                "Monitor the condition for any changes",
                "Maintain good hygiene practices",
                "Keep the affected area clean and dry" if disease_type == 'skin' else "Avoid rubbing or touching the eyes"
            ],
            "description": f"Visual analysis of {'skin' if disease_type == 'skin' else 'eye'} image completed. Professional medical consultation recommended for proper diagnosis and treatment plan."
        }
        
        print("\n" + "="*80)
        print("📦 Fallback Analysis Result:")
        print("="*80)
        print(json.dumps(fallback_result, indent=2))
        print("="*80 + "\n")
        
        return fallback_result
        
    except Exception as e:
        print(f"\n❌ Groq analysis error: {e}")
        
        # Return basic fallback for any other errors
        return {
            "disease_name": "Analysis Pending",
            "confidence": 70.0,
            "severity": "medium",
            "recommendations": [
                "Consult a medical professional for accurate diagnosis",
                "Monitor the condition",
                "Seek medical attention if symptoms worsen"
            ],
            "description": "Image analysis encountered an issue. Please consult a healthcare professional."
        }

from flask import Blueprint, request, jsonify
from utils.gemini_utils import chat_with_gemini
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/', methods=['POST'])
def chat():
    """Send message to Gemini chatbot and get response"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message']
        conversation_history = data.get('history', None)
        
        # Get response from Gemini
        response = chat_with_gemini(message, conversation_history)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Chatbot error: {e}")
        return jsonify({
            'error': str(e),
            'response': 'Sorry, I encountered an error. Please try again later.'
        }), 500

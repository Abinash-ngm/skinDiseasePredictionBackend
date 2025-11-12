from flask import Blueprint, request, jsonify
from utils.gemini_utils import chat_with_gemini
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/', methods=['POST'])
def chat():
    """Send message to Gemini chatbot and get response"""
    try:
        data = request.get_json()
        
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
        return jsonify({'error': str(e)}), 500

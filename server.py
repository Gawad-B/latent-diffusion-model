from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Google Gemini API configuration
GOOGLE_API_KEY = "AIzaSyA9NqF58IsYrU3Djj-xsj4yoenBRIW0ZgM"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"

USE_GEMINI = True

# System context for the AI
SYSTEM_CONTEXT = """You are an AI assistant for medical information. 
Your role is to help users with medical questions and health-related information.

If a question falls outside your area of medical expertise, respond with:
"As an AI assistant for medical information, the question about [topic] falls outside my area of expertise and purpose."

FORMATTING INSTRUCTIONS:
1. Write in plain text - do NOT use **bold** or any markdown formatting
2. Write complete sentences and paragraphs naturally
3. Use simple, clear language
4. Separate paragraphs with a blank line
5. For lists, start each item with * followed by a space
6. Section headers should end with a colon

Example:
Eczema, also known as atopic dermatitis, is a chronic skin condition that causes itchy, dry, and inflamed skin.

Key symptoms:
* Intense itching
* Red patches
* Dry, scaly skin

Be professional, clear, and helpful."""

def get_ai_response(user_message):
    """Get response from Google Gemini API using REST"""
    
    if not USE_GEMINI:
        return get_fallback_response(user_message)
    
    try:
        # Create a prompt with context
        prompt = f"{SYSTEM_CONTEXT}\n\nUser question: {user_message}\n\nAssistant:"
        
        # Prepare the request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        # Make the API request
        response = requests.post(
            GEMINI_API_URL,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract the text from the response
            if 'candidates' in data and len(data['candidates']) > 0:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        return parts[0]['text']
            
            # If we couldn't extract text, check for safety issues
            if 'promptFeedback' in data:
                print(f"Prompt feedback: {data['promptFeedback']}")
            
            return "I received your message but couldn't generate a proper response. Could you please rephrase your question?"
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return get_fallback_response(user_message)
            
    except requests.exceptions.Timeout:
        print("API request timed out")
        return get_fallback_response(user_message)
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback responses when API fails"""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm here to help you with information about rare diseases and medical imaging. How can I assist you?"
    elif any(word in message_lower for word in ['rare disease', 'rare condition']):
        return "Rare diseases affect fewer than 200,000 people in the US. Our database contains medical images for various rare conditions to aid in research and diagnosis."
    elif any(word in message_lower for word in ['imaging', 'image', 'scan']):
        return "Medical imaging includes techniques like X-rays, CT scans, MRI, and ultrasound. Our database contains images from various modalities for research purposes."
    elif any(word in message_lower for word in ['database', 'data']):
        return "Our database is a comprehensive collection of medical images for rare diseases, carefully curated and annotated for research use."
    else:
        return "I'm here to help with information about rare diseases, medical imaging, and our database. What would you like to know?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test-api', methods=['GET'])
def test_api():
    """Test endpoint to verify API key works"""
    if not USE_GEMINI:
        return jsonify({
            'status': 'fallback',
            'message': 'Gemini API not available, using fallback responses',
            'gemini_enabled': False
        })
    
    try:
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Say 'Hello' in one word"
                }]
            }]
        }
        
        response = requests.post(
            GEMINI_API_URL,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = "No text in response"
            
            if 'candidates' in data and len(data['candidates']) > 0:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        response_text = parts[0]['text']
            
            return jsonify({
                'status': 'success',
                'message': 'API is working',
                'gemini_enabled': True,
                'test_response': response_text
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f"API returned status {response.status_code}",
                'gemini_enabled': False,
                'details': response.text
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'gemini_enabled': False
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get AI response
    ai_response = get_ai_response(user_message)
    
    return jsonify({'response': ai_response})

@app.route('/generate', methods=['POST'])
def generate():
    """Handle image generation requests"""
    data = request.get_json()
    disease = data.get('disease', '')
    count = data.get('count', 1)
    
    if not disease:
        return jsonify({'success': False, 'error': 'No disease specified'}), 400
    
    try:
        # TODO: Replace this with actual image generation logic
        # For now, return placeholder response
        generated_images = []
        
        # Placeholder: You would integrate your latent diffusion model here
        # Example: generated_images = generate_medical_images(disease, count)
        
        # For demonstration, return dummy image paths
        for i in range(count):
            # This is a placeholder - replace with actual generated image paths
            generated_images.append(f'/static/images/generated_{disease}_{i+1}.jpg')
        
        return jsonify({
            'success': True,
            'images': generated_images,
            'disease': disease,
            'count': count
        })
    
    except Exception as e:
        print(f"Error generating images: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
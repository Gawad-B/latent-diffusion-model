from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
import requests
import json
import os
from pathlib import Path
import base64
from io import BytesIO
import zipfile
import time
from dotenv import load_dotenv
from functools import wraps
from database import db, User

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Model generator (lazy loaded)
model_generator = None

# Google Gemini API configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
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

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@app.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    """Handle user registration"""
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Validation
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return jsonify({'error': 'Failed to create account'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Set session
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify({'success': True, 'message': 'Login successful', 'username': user.username})

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

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
    global model_generator
    
    data = request.get_json()
    disease = data.get('disease', '')
    count = data.get('num_images', data.get('count', 1))
    
    if not disease:
        return jsonify({'success': False, 'error': 'No disease specified'}), 400
    
    # Validate count
    count = int(count)
    if count < 1 or count > 20:
        return jsonify({'success': False, 'error': 'Count must be between 1 and 20'}), 400
    
    # Limit display to maximum 6 samples
    display_count = min(count, 6)
    
    try:
        # Lazy load model generator
        if model_generator is None:
            from model_inference import MedicalImageGenerator
            checkpoint_path = Path('./checkpoints/final_unet_model.pth')
            
            # Check if checkpoint exists
            if not checkpoint_path.exists():
                return jsonify({
                    'success': False,
                    'error': 'Model checkpoint not found. Please train the model first or download the trained weights.'
                }), 500
            
            print("Loading model... (this may take a minute)")
            model_generator = MedicalImageGenerator(model_path=checkpoint_path)
            print("Model loaded successfully!")
        
        # Generate images
        output_dir = Path('./static/generated').resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a unique session folder
        session_id = f"{disease}_{int(time.time())}"
        session_dir = output_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate images
        saved_paths = model_generator.generate_images(
            num_images=count,
            disease_type=disease,
            save_path=session_dir
        )
        
        # Convert to web-accessible paths
        web_paths = []
        for path in saved_paths:
            # Get the absolute path and ensure it's within static/generated
            abs_path = Path(path).resolve()
            
            # Verify the path is within our allowed directory
            if not str(abs_path).startswith(str(output_dir)):
                raise ValueError(f"Generated file path is not in allowed directory")
            
            # Create web path: /static/generated/session_id/filename.png
            # Get relative path from project root to the image
            project_root = Path.cwd()
            rel_path = abs_path.relative_to(project_root)
            web_path = '/' + str(rel_path).replace('\\', '/')
            web_paths.append(web_path)
        
        # Limit displayed images to maximum 6 samples
        display_paths = web_paths[:display_count]
        
        return jsonify({
            'success': True,
            'images': display_paths,
            'disease': disease,
            'count': count,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"Error generating images: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/download-batch', methods=['POST'])
def download_batch():
    """Download all generated images as a zip file"""
    data = request.get_json()
    session_id = data.get('session_id', '')
    
    if not session_id:
        return jsonify({'success': False, 'error': 'No session ID provided'}), 400
    
    try:
        session_dir = Path('./static/generated') / session_id
        
        if not session_dir.exists():
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Create zip file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for img_file in session_dir.glob('*.png'):
                zf.write(img_file, img_file.name)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{session_id}_images.zip'
        )
    
    except Exception as e:
        print(f"Error creating zip: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/download-all/<session_id>', methods=['GET'])
@login_required
def download_all(session_id):
    """Download all generated images as a zip file"""
    if not session_id:
        return jsonify({'success': False, 'error': 'No session ID provided'}), 400
    
    try:
        session_dir = Path('./static/generated') / session_id
        
        if not session_dir.exists():
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Create zip file in memory
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for img_file in session_dir.glob('*.png'):
                zf.write(img_file, img_file.name)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'{session_id}_images.zip'
        )
    
    except Exception as e:
        print(f"Error creating zip: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
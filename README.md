# RDMID - Rare Diseases Medical Images Database

A web application for managing and generating medical images for rare diseases using AI technology. This platform provides a comprehensive database of medical images and leverages AI to generate synthetic medical images for research, diagnosis, and educational purposes.

## Features

### 🗂️ Medical Image Database
- Curated collection of medical images for rare diseases
- Carefully organized and annotated for research purposes
- Support for various imaging modalities (X-ray, CT, MRI)

### 🧠 AI-Powered Image Generation
- Generate synthetic medical images using advanced AI models
- Support for multiple rare diseases (Pneumonia, Tuberculosis)
- Batch generation capability (1-10 images)
- Image upload functionality (PDF, JPG, JPEG, PNG)

### 💬 AI Chat Assistant
- Interactive chat interface powered by Google Gemini AI
- Get instant answers about rare diseases and medical imaging
- Context-aware responses about the database and research

### 🔒 Data Privacy
- All images are properly anonymized
- Compliance with medical data privacy standards

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **AI Integration**: Google Gemini API (gemini-2.5-flash)
- **Icons**: Font Awesome
- **Responsive Design**: CSS Flexbox

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gawad-B/latent-diffusion-model.git
cd latent-diffusion-model
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google Gemini API key in `server.py`:
```python
GOOGLE_API_KEY = "your-api-key-here"
```

4. Run the application:
```bash
python server.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
latent-diffusion-model/
├── server.py                 # Flask backend server
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Main HTML template
├── static/
│   ├── assets/
│   │   ├── css/
│   │   │   └── main.css    # Stylesheets
│   │   ├── js/
│   │   │   └── main.js     # Custom JavaScript
│   │   └── webfonts/       # Font files
│   └── images/
│       └── lungs.ico       # Favicon
```

## API Endpoints

### `GET /`
Serves the main web application.

### `POST /chat`
Handles AI chat interactions.
- **Request**: `{"message": "your message"}`
- **Response**: `{"response": "AI response"}`

### `POST /generate`
Generates medical images based on selected disease.
- **Request**: `{"disease": "disease_name", "num_images": number}`
- **Response**: `{"images": ["image1.jpg", "image2.jpg", ...]}`

### `GET /test-api`
Tests Google Gemini API connectivity.

## Usage

### Generating Medical Images
1. Navigate to the "Generate Images" section
2. Select a rare disease from the dropdown
3. Specify the number of images to generate (1-10)
4. Optionally upload a reference image
5. Click "Generate Images"

### Using the AI Chat
1. Navigate to the "AI Chat" section
2. Type your question in the input field
3. Press "Send" to get instant AI-powered responses
4. Continue the conversation as needed

## Features in Development

- Integration of actual latent diffusion model for medical image generation
- Backend processing for uploaded images
- Expanded disease database
- Advanced image analysis tools
- Enhanced data privacy features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

© Gawad. All rights reserved.

## Author

**Abdelrahman Gawad**
- Portfolio: [https://gawad163.pythonanywhere.com/](https://gawad163.pythonanywhere.com/)
- GitHub: [@Gawad-B](https://github.com/Gawad-B)

## Acknowledgments

- Google Gemini AI for powering the chat assistant
- Font Awesome for icons
- Medical research community for inspiration

---

**Note**: This application is intended for research and educational purposes. Always consult qualified healthcare professionals for medical decisions.

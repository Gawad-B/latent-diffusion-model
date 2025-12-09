# RDMID - Rare Diseases Medical Images Database

A comprehensive web application for managing and generating medical images for rare diseases using AI technology. This platform provides a medical images database and leverages **Latent Diffusion Models** to generate synthetic chest X-ray images for research, diagnosis, and educational purposes.

## 🎉 Features Complete!

Your medical image generation system is fully integrated and ready to use with authentication!

## ✨ Key Features

### 🔐 User Authentication
- **Secure Login & Signup** with liquid glass UI design
- Password hashing with Werkzeug
- Session-based authentication
- Protected routes requiring login
- User database with SQLite

### 🧬 AI Medical Image Generation
- **Latent Diffusion Model** trained on chest X-ray datasets
- Generate synthetic images for:
  - Normal (healthy) chest X-rays
  - Pneumonia cases
  - Tuberculosis cases
- **Batch generation**: Create 1-10 images at once
- **Preview before download**: Review quality before saving
- **Flexible downloads**: Individual images or bulk ZIP download

### 💬 AI Chat Assistant
- Interactive medical information assistant powered by **Google Gemini 2.5 Flash**
- Get instant answers about rare diseases and medical imaging
- Context-aware responses with medical expertise
- Environment variable-based API key management

### 🗂️ Medical Image Database
- Curated collection of medical images for rare diseases
- Support for various imaging modalities (X-ray, CT, MRI)
- Organized and annotated for research purposes

### 🔒 Data Privacy
- All images are properly anonymized
- Compliance with medical data privacy standards

## 🏗️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with Flask-SQLAlchemy
- **Authentication**: Session-based with Werkzeug password hashing
- **ML Framework**: PyTorch + Diffusers (Hugging Face)
- **Model**: Latent Diffusion Model (U-Net + VAE)
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **AI Chat**: Google Gemini API (gemini-2.5-flash)
- **Design**: Responsive CSS with glassmorphism effects & Font Awesome icons
- **Security**: Environment variables with python-dotenv, Git LFS for large files

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Gawad-B/latent-diffusion-model.git
cd latent-diffusion-model
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
⏱️ *Note: First installation may take 5-10 minutes (downloads PyTorch, etc.)*

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key_for_sessions
```

### 4. Get the Trained Model
**IMPORTANT:** Download the trained model from your Colab notebook.

See **[MODEL_DOWNLOAD_GUIDE.md](MODEL_DOWNLOAD_GUIDE.md)** for detailed instructions.

Quick version:
1. Open `Copy of Tuberculosis_&_Pneumonia_.ipynb` in Colab
2. Download `final_unet_model.pth` (or `model_checkpoints.zip`)
3. Place in `checkpoints/` folder

### 5. Verify Setup
```bash
python verify_setup.py
```

### 6. Start the Server
```bash
python server.py
```

### 7. Create Your Account
1. Open `http://127.0.0.1:5000/signup`
2. Fill in username, email, and password
3. Click the liquid glass "Sign Up" button

### 8. Login and Use
1. Navigate to `http://127.0.0.1:5000/login`
2. Enter your credentials
3. Start generating images and chatting with AI!

## 📂 Project Structure

```
latent-diffusion-model/
├── server.py                           # Flask backend server with authentication
├── database.py                         # User database models
├── model_inference.py                  # ML model inference engine
├── requirements.txt                    # Python dependencies
├── verify_setup.py                     # Setup verification script
├── .env                                # Environment variables (API keys, secrets)
├── .gitignore                          # Git ignore file
├── README.md                           # Complete documentation (this file)
├── Copy of Tuberculosis_&_Pneumonia_.ipynb  # Colab training notebook
├── checkpoints/
│   ├── .gitattributes                 # Git LFS configuration
│   └── final_unet_model.pth           # Trained model weights (385MB, tracked with Git LFS)
├── static/
│   ├── generated/                     # Generated images (auto-created)
│   ├── images/                        # Static images (logo, favicon)
│   ├── assets/
│   │   ├── css/main.css              # Stylesheets
│   │   ├── js/main.js                # Custom JavaScript
│   │   └── webfonts/                 # Font files
└── templates/
    ├── index.html                     # Main application page (protected)
    ├── login.html                     # Login page with liquid glass button
    └── signup.html                    # Signup page with liquid glass button
│   │   └── webfonts/                 # Font files
└── templates/
    └── index.html                     # Main HTML template
```
└── INTEGRATION_COMPLETE.md            # Integration summary
```

## 🎯 How to Use

### First Time Setup
1. **Sign Up**: Navigate to `/signup` and create an account
2. **Login**: Use your credentials at `/login`
3. **Access Protected Features**: All image generation and chat features require login

### Generating Medical Images

1. **Navigate** to the "Generate Images" section
2. **Select disease type:**
   - Normal (healthy chest X-ray)
   - Pneumonia
   - Tuberculosis
3. **Choose quantity:** 1-10 images
4. **Click "Generate Images"**
5. **Wait** ~30-60 seconds (GPU) or 3-5 minutes (CPU)
6. **Preview** all generated images in a grid
7. **Download:**
   - Individual images: Click download button on each
   - Bulk download: Click "Download All as ZIP"

### Using the AI Chat Assistant

1. Navigate to the "AI Chat" section
2. Type your medical question
3. Press "Send" or hit Enter
4. Get instant AI-powered responses about:
   - Rare diseases
   - Medical imaging
   - Research information

## 🔌 API Endpoints

### Authentication

#### `GET /login`
Serves the login page with liquid glass button design.

#### `GET /signup`
Serves the signup page with liquid glass button design.

#### `POST /api/login`
User login endpoint.
- **Request**: `{"email": "user@example.com", "password": "password123"}`
- **Response**: `{"success": true, "message": "Login successful", "username": "user"}`

#### `POST /api/signup`
User registration endpoint.
- **Request**: `{"username": "user", "email": "user@example.com", "password": "password123"}`
- **Response**: `{"success": true, "message": "Account created successfully"}`

#### `POST /api/logout`
User logout endpoint.
- **Response**: `{"success": true, "message": "Logged out successfully"}`

### Application Routes

### `GET /`
Serves the main web application (requires login).

### `POST /chat`
AI chat interactions.
- **Request**: `{"message": "your question"}`
- **Response**: `{"response": "AI answer"}`

### `POST /generate`
Generates medical images.
- **Request**: `{"disease": "pneumonia", "count": 5}`
- **Response**: `{"success": true, "images": [...], "session_id": "..."}`

### `POST /download-batch`
Downloads all generated images as ZIP.
- **Request**: `{"session_id": "pneumonia_1234567890"}`
- **Response**: ZIP file download

### `GET /test-api`
Tests Google Gemini API connectivity.

## 🤖 Model Details

### Architecture
- **Type**: Latent Diffusion Model
- **Components**:
  - VAE (Variational Autoencoder): Stable Diffusion VAE
  - U-Net: Custom 2D U-Net with attention blocks
- **Image Resolution**: 256×256 pixels (grayscale)
- **Latent Dimensions**: 32×32×4 channels
- **Training Data**: Kaggle chest X-ray datasets (Pneumonia + TB)

### Performance
- **GPU (CUDA)**: ~30-60 seconds for 4 images
- **CPU**: ~3-5 minutes for 4 images
- **Model Size**: ~500 MB
- **Memory Required**: 2-4 GB RAM

### Quality Metrics
- FID Score: <50 (good quality)
- Inference Steps: 50 (configurable)

## 📚 Documentation

All documentation has been integrated into this README. Previously separate guides:
- ~~SETUP.md~~ - Now in "Installation & Setup" section below
- ~~MODEL_DOWNLOAD_GUIDE.md~~ - Now in "Getting the Trained Model" section below
- ~~INTEGRATION_COMPLETE.md~~ - Now in "What Was Implemented" section below

---

# 📖 Complete Setup Guide

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended) or CPU
- At least 8GB RAM (16GB recommended)
- Internet connection for downloading dependencies

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Gawad-B/latent-diffusion-model.git
cd latent-diffusion-model
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
⏱️ **Note:** First installation may take 5-10 minutes as it downloads PyTorch and other ML libraries.

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key_for_sessions
```
**Note:** The `.env` file is already in `.gitignore` to keep your secrets safe.

### 4. Get the Trained Model

**CRITICAL:** You need to download the trained model checkpoint from your Colab notebook!

**Note:** The model file (385MB) is tracked with **Git LFS** for version control.

#### Quick Guide: Getting Your Model from Colab

**Step 1: Locate the Model in Your Colab Notebook**

In `Copy of Tuberculosis_&_Pneumonia_.ipynb`, look for the cell that saves the model:

```python
# Save Final Model
final_model_path = config.CHECKPOINT_DIR / "final_unet_model.pth"
torch.save(model.state_dict(), final_model_path)
```

**Step 2: Download the Model File**

Choose one of these options:

##### Option A: Direct Download from Colab

Add and run this cell at the end of your notebook:

```python
from google.colab import files

# Download the final model
files.download('./checkpoints/final_unet_model.pth')
```

This will trigger a download in your browser.

##### Option B: Download the Pre-created ZIP

The notebook already creates a zip file. Run this cell:

```python
from google.colab import files

# Download the model checkpoints zip
files.download('model_checkpoints.zip')
```

Then extract the zip file on your local machine.

##### Option C: Use Google Drive

If the file is too large for direct download:

1. Mount Google Drive in Colab (if not already):
```python
from google.colab import drive
drive.mount('/content/drive')
```

2. Copy the model to Drive:
```python
import shutil
shutil.copy(
    './checkpoints/final_unet_model.pth',
    '/content/drive/MyDrive/final_unet_model.pth'
)
print("✓ Model copied to Google Drive!")
```

3. Go to your Google Drive and download the file
4. Place it in your local `checkpoints/` folder

**Step 3: Verify the Download**

The file should be approximately **400-600 MB** in size.

Check the file on your local machine:

```bash
# On Linux/Mac
ls -lh checkpoints/final_unet_model.pth

# On Windows
dir checkpoints\final_unet_model.pth
```

**Step 4: Place in Correct Location**

Move the downloaded file to your project:

```
latent-diffusion-model/
├── checkpoints/
│   └── final_unet_model.pth  ← Put it here!
```

### 4. Verify Directory Structure

Ensure your project has this structure:

```
latent-diffusion-model/
├── server.py
├── database.py
├── model_inference.py
├── requirements.txt
├── verify_setup.py
├── .env  ← Your environment variables (create this!)
├── checkpoints/
│   └── final_unet_model.pth  ← Your trained model (REQUIRED)
├── static/
│   ├── generated/  ← Generated images saved here (auto-created)
│   └── assets/
├── templates/
│   ├── index.html
│   ├── login.html
│   └── signup.html
└── Copy of Tuberculosis_&_Pneumonia_.ipynb
```

### 5. Test the Model (Optional)

Test if the model loads correctly:

```bash
python model_inference.py
```

You should see:
```
Using device: cuda (or cpu)
Loading VAE...
Creating U-Net model...
Loading checkpoint from: checkpoints/final_unet_model.pth
Checkpoint loaded successfully!
Model initialized successfully!
```

### 6. Verify Complete Setup

```bash
python verify_setup.py
```

This checks all dependencies, files, and configurations.

### 7. Start the Server
```bash
python server.py
```

The server will start on `http://127.0.0.1:5000`

### 8. Open Your Browser
```
http://127.0.0.1:5000
```

Navigate to "Generate Images" and start creating synthetic medical images!

---

# 🎯 How to Use the Application

## Generating Medical Images

### User Flow:
```
1. Select disease → 2. Set image count → 3. Click "Generate"
                                                     ↓
4. Loading indicator (30s-5min) ← 5. Model generates images
                                                     ↓
6. Preview all images ← 7. Review quality
                                                     ↓
8. Download individual images or all as ZIP
```

### Step-by-Step:

1. **Navigate** to the "Generate Images" section
2. **Select disease type:**
   - Normal (healthy chest X-ray)
   - Pneumonia
   - Tuberculosis
3. **Choose quantity:** 1-10 images
4. **Click "Generate Images"**
5. **Wait for generation:**
   - GPU: ~30-60 seconds
   - CPU: ~3-5 minutes
6. **Preview** all generated images in a grid
7. **Download:**
   - Individual images: Click download button on each
   - Bulk download: Click "Download All as ZIP"

### First Run Notes

- First generation loads the model into memory (~2GB)
- Initial load takes 30-60 seconds
- Subsequent generations are faster

## Using the AI Chat Assistant

1. Navigate to the "AI Chat" section
2. Type your medical question
3. Press "Send" or hit Enter
4. Get instant AI-powered responses about:
   - Rare diseases
   - Medical imaging
   - Research information

---

# 🔌 API Endpoints

## `GET /`
Serves the main web application.

## `POST /chat`
AI chat interactions.
- **Request**: `{"message": "your question"}`
- **Response**: `{"response": "AI answer"}`

## `POST /generate`
Generates medical images.
- **Request**: 
  ```json
  {
    "disease": "pneumonia",
    "count": 5
  }
  ```
- **Response**: 
  ```json
  {
    "success": true,
    "images": ["/static/generated/session_id/image1.png", ...],
    "session_id": "pneumonia_1234567890",
    "disease": "pneumonia",
    "count": 5
  }
  ```

### Example API Usage:
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"disease": "pneumonia", "count": 3}'
```

## `POST /download-batch`
Downloads all generated images as ZIP.
- **Request**: 
  ```json
  {
    "session_id": "pneumonia_1234567890"
  }
  ```
- **Response**: ZIP file download

### Example API Usage:
```bash
curl -X POST http://localhost:5000/download-batch \
  -H "Content-Type: application/json" \
  -d '{"session_id": "pneumonia_1234567890"}' \
  --output images.zip
```

## `GET /test-api`
Tests Google Gemini API connectivity.
- **Response**: 
  ```json
  {
    "status": "success",
    "message": "API is working",
    "gemini_enabled": true
  }
  ```

---

# 🤖 Model Details & Technical Specifications

### What Was Implemented

### 1. User Authentication System (`database.py`, `server.py`)
- SQLite database with Flask-SQLAlchemy
- User model with secure password hashing
- Login/signup pages with liquid glass button design
- Session-based authentication
- Protected routes with `@login_required` decorator
- Logout functionality

### 2. Model Integration (`model_inference.py`)
- Loads the trained Latent Diffusion Model from Colab notebook
- Uses Stable Diffusion VAE for image encoding/decoding
- Generates synthetic chest X-ray images
- Supports batch generation with progress tracking

### 3. Backend API (`server.py`)
- Authentication endpoints: `/api/login`, `/api/signup`, `/api/logout`
- `/generate` endpoint: Generates images based on disease type and count
- `/download-batch` endpoint: Downloads all generated images as ZIP
- Lazy-loads the model (saves memory)
- Creates unique session folders for each generation batch
- Environment variable configuration with `.env`

### 4. Frontend Interface (`static/assets/js/main.js`, templates)
- Login/signup pages with liquid glass glassmorphism button design
- User selects disease type and image count
- Shows loading indicator during generation
- Preview mode displays all generated images in grid
- Individual download buttons for each image
- "Download All as ZIP" button for batch download
- Smooth scrolling to results
- Logout button in sidebar

## Architecture

### Model Components:
- **Type**: Latent Diffusion Model (LDM)
- **VAE (Variational Autoencoder)**: Stable Diffusion VAE (pre-trained)
  - Compresses 256×256 images → 32×32×4 latents
  - Reduces computational cost dramatically
- **U-Net**: Custom 2D U-Net with attention blocks
  - Predicts noise in latent space
  - Attention mechanisms for global context
- **Scheduler**: DDPM (Denoising Diffusion Probabilistic Model)
  - 1000 training timesteps
  - 50 inference steps (configurable)

### Specifications:
- **Image Resolution**: 256×256 pixels (grayscale)
- **Latent Dimensions**: 32×32×4 channels
- **Model Size**: ~500 MB
- **Training Data**: Kaggle chest X-ray datasets (Pneumonia + TB)

### Performance Metrics:
- **GPU (CUDA)**: ~30-60 seconds for 4 images
- **CPU**: ~3-5 minutes for 4 images
- **Memory Required**: 2-4 GB RAM
- **FID Score**: <50 (good quality)
- **Inference Steps**: 50 (configurable for speed/quality tradeoff)

### Supported Diseases:
- Normal (healthy chest X-ray)
- Pneumonia
- Tuberculosis

## Model Configuration

Current settings (in `model_inference.py`):

```python
class Config:
    VAE_MODEL = "stabilityai/sd-vae-ft-mse"
    VAE_SCALE_FACTOR = 0.18215
    LATENT_SIZE = 32  # 256 // 8
    LATENT_CHANNELS = 4
    IMAGE_SIZE = 256
    TIMESTEPS = 1000
    NUM_INFERENCE_STEPS = 50  # Adjustable
```

### Adjusting Generation Quality

Edit `model_inference.py` to change:

```python
# Faster but lower quality
NUM_INFERENCE_STEPS = 25  # Default: 50

# Slower but higher quality  
NUM_INFERENCE_STEPS = 100
```

---

# 🐛 Troubleshooting

## Common Issues

| Problem | Solution |
|---------|----------|
| "Model checkpoint not found" | Download `final_unet_model.pth` from Colab (see "Getting the Trained Model" above) |
| Slow generation | Normal on CPU; use GPU or reduce image count |
| "CUDA out of memory" | Generate fewer images at once (1-2 instead of 10) or force CPU mode |
| Import errors | Run `pip install -r requirements.txt` |
| Images look random/noisy | Model not properly trained - retrain for more epochs; Check FID score should be < 50 |

## Detailed Troubleshooting

### Error: "Model checkpoint not found"

**Solution:** Make sure `final_unet_model.pth` is in the `checkpoints/` folder.

Run this to check:
```bash
ls -la checkpoints/
```

### Error: "CUDA out of memory"

**Solution:** 
- Generate fewer images at once (1-2 instead of 10)
- Or force CPU mode by modifying `model_inference.py`:
  ```python
  self.device = torch.device("cpu")  # Force CPU
  ```

### Error: "No module named 'diffusers'"

**Solution:** Install dependencies again:
```bash
pip install -r requirements.txt
```

### Model Download Issues

#### "File not found" in Colab

Run this in a Colab cell to see where files are:
```python
!ls -la checkpoints/
```

Look for files ending in `.pth`

#### File is too small (< 100 MB)

Model didn't train properly. You need to:
1. Re-run the training cells in the notebook
2. Wait for all epochs to complete
3. Then download again

#### "Checkpoint loading error" 

The model architecture must match. Don't modify `model_inference.py` architecture without ensuring compatibility.

### Performance Issues

Run `python verify_setup.py` to check your setup and get recommendations.

---

# 🔬 Training Your Own Model

## Training from Scratch

1. Open `Copy of Tuberculosis_&_Pneumonia_.ipynb` in Google Colab
2. Run all cells sequentially
3. Training takes ~3-6 hours on T4 GPU (Colab)
4. Download the checkpoint when complete
5. Place in `checkpoints/` folder

## Training Parameters

Current training settings:
- **Epochs**: 70
- **Batch Size**: 32
- **Learning Rate**: 1e-4
- **Optimizer**: AdamW
- **Loss**: MSE (Mean Squared Error)

## Datasets Used

- [Chest X-Ray Pneumonia Dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- [Tuberculosis Dataset](https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset)

---

## ✨ Features Implemented

✅ **User Authentication**: Secure login/signup with session management  
✅ **Liquid Glass UI**: Modern glassmorphism design for auth buttons  
✅ **Password Security**: Werkzeug password hashing  
✅ **Protected Routes**: All main features require authentication  
✅ **Disease Selection**: Choose Normal, Pneumonia, or Tuberculosis  
✅ **Batch Generation**: Generate 1-10 images at once  
✅ **Progress Indicator**: Visual feedback during generation  
✅ **Image Preview**: See all generated images before downloading  
✅ **Individual Download**: Download specific images  
✅ **Batch Download**: Download all as ZIP file  
✅ **Session Management**: Each generation gets unique folder  
✅ **Error Handling**: Graceful error messages  
✅ **Responsive UI**: Works on desktop and mobile  
✅ **AI Chat Assistant**: Google Gemini powered medical Q&A  
✅ **Lazy Loading**: Model loads only when needed  
✅ **Environment Variables**: Secure API key management  
✅ **Git LFS Integration**: Large model file version control

---

# 🛣️ Roadmap

## Completed
- [x] Latent Diffusion Model integration
- [x] Image generation pipeline
- [x] Preview before download
- [x] Batch ZIP download
- [x] AI Chat Assistant (Google Gemini 2.5 Flash)
- [x] Responsive web interface
- [x] User authentication system
- [x] Login/signup with liquid glass design
- [x] Session management
- [x] Protected routes
- [x] Environment variable configuration
- [x] Git LFS for large files

## Planned
- [ ] Password reset functionality
- [ ] Email verification
- [ ] User profile management
- [ ] Generation history per user
- [ ] Conditional generation (specify exact features)
- [ ] Super-resolution upscaling (256→1024)
- [ ] Multiple disease categories
- [ ] Image-to-image translation
- [ ] User accounts and history
- [ ] Generation gallery
- [ ] Enhanced data privacy features
- [ ] RESTful API documentation
- [ ] Docker containerization

---

# 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Submit a pull request

---

# 📄 License

© Gawad. All rights reserved.

---

# 👨‍💻 Author

**Abdelrahman Gawad**
- Portfolio: [https://gawad163.pythonanywhere.com/](https://gawad163.pythonanywhere.com/)
- GitHub: [@Gawad-B](https://github.com/Gawad-B)

---

# 🙏 Acknowledgments

- **Model Architecture**: Based on "High-Resolution Image Synthesis with Latent Diffusion Models" (Rombach et al., CVPR 2022)
- **Datasets**: Kaggle Medical Imaging Datasets
  - [Chest X-Ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
  - [Tuberculosis Dataset](https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset)
- **AI Chat**: Google Gemini API
- **VAE**: Stability AI's Stable Diffusion VAE
- **Design**: HTML5 UP Template
- **Icons**: Font Awesome
- Medical research community for inspiration

---

# ⚠️ Disclaimer

This tool is for **research and educational purposes only**. Generated images should **not be used for clinical diagnosis**. Always consult qualified medical professionals for medical advice and decisions.

---

# 🚀 Quick Start Summary

```bash
# 1. Clone repo
git clone https://github.com/Gawad-B/latent-diffusion-model.git
cd latent-diffusion-model

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
# Create .env file with:
# GOOGLE_API_KEY=your_api_key
# SECRET_KEY=your_secret_key

# 4. Download model from Colab (see "Getting the Trained Model" section)
# Place final_unet_model.pth in checkpoints/

# 5. Verify setup
python verify_setup.py

# 6. Start server
python server.py

# 7. Create account and login
# Navigate to http://127.0.0.1:5000/signup
# Then login at http://127.0.0.1:5000/login
```

**Ready to generate medical images!** 🏥🖼️✨

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Model checkpoint not found" | Download from Colab (see MODEL_DOWNLOAD_GUIDE.md) |
| Slow generation | Normal on CPU; use GPU or reduce count |
| "CUDA out of memory" | Generate fewer images at once |
| Import errors | Run `pip install -r requirements.txt` |

Run `python verify_setup.py` to check your setup.

## 🔬 Training Your Own Model

1. Open `Copy of Tuberculosis_&_Pneumonia_.ipynb` in Google Colab
2. Run all cells sequentially
3. Training takes ~3-6 hours on T4 GPU
4. Download checkpoint when complete
5. Place in `checkpoints/` folder

## 🛣️ Roadmap

- [x] Latent Diffusion Model integration
- [x] Image generation pipeline
- [x] Preview before download
- [x] Batch ZIP download
- [ ] Conditional generation (specify exact features)
- [ ] Super-resolution upscaling (256→1024)
- [ ] Multiple disease categories
- [ ] Image-to-image translation
- [ ] User accounts and history
- [ ] Enhanced data privacy features

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

© Gawad. All rights reserved.

## 👨‍💻 Author

**Abdelrahman Gawad**
- Portfolio: [https://gawad-b.github.io/](https://gawad-b.github.io/)
- GitHub: [@Gawad-B](https://github.com/Gawad-B)

## 👥 Team & Contributors

**Project Team:**
- **[Abdelrahman Gawad]** - [Full Stack Web Development]
- **[Omar Elwekeil]** - [Role/Contribution]
- **[Ahmed Mostafa]** - [Role/Contribution]
- **[Martina Maher]** - [Role/Contribution]
- **[Rahma Asem]** - [Role/Contribution]
- **[Reem Tarek]** - [Role/Contribution]

## 🙏 Acknowledgments

- **Model Architecture**: Based on "High-Resolution Image Synthesis with Latent Diffusion Models" (CVPR 2022)
- **Datasets**: Kaggle Medical Imaging Datasets
  - [Chest X-Ray Pneumonia](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
  - [Tuberculosis Dataset](https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset)
- **AI Chat**: Google Gemini API
- **Design**: Figma
- **Icons**: Font Awesome
- Medical research community for inspiration

## ⚠️ Disclaimer

This tool is for research and educational purposes only. Generated images should not be used for clinical diagnosis. Always consult qualified medical professionals for medical advice and decisions.

---

**Ready to generate medical images?** Get started with the [Setup Guide](SETUP.md)! 🚀

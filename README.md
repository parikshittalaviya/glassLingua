# 🔍 glassLingua

**An AI-powered multilingual book reading assistant that bridges the gap between visual text and audio accessibility.**

glassLingua is an innovative Python application that uses computer vision, OCR, and AI translation to detect books, extract text, translate content, and provide audio feedback in multiple Indian languages. Perfect for accessibility, language learning, and multilingual content consumption.

## ✨ Features

### 🎯 Core Functionality
- **Smart Book Detection**: Uses YOLO v3 to detect and validate complete books in camera feed
- **Advanced OCR**: Leverages Google Cloud Vision API for accurate text extraction
- **AI Text Enhancement**: Integrates Google Gemini AI to refine and correct extracted text
- **Multi-language Translation**: Supports 9 languages including Hindi, Gujarati, English, and more
- **Voice-to-Voice Interface**: Speech recognition for language selection and text-to-speech output
- **Real-time Processing**: Live camera feed with instant feedback

### 🌐 Supported Languages
- **Hindi** (हिन्दी)
- **Gujarati** (ગુજરાતી) 
- **English**
- **Punjabi** (ਪੰਜਾਬੀ)
- **Bengali** (বাংলা)
- **Kannada** (ಕನ್ನಡ)
- **Marathi** (मराठी)
- **Tamil** (தமிழ்)
- **Telugu** (తెలుగు)

## 🏗️ Architecture

The application follows a modular architecture with distinct components:

```
glassLingua/
├── main.py              # Main application orchestrator
├── vision.py            # YOLO-based book detection & camera handling
├── ocr_module.py        # Google Vision OCR & Gemini text enhancement
├── translation.py       # Multi-language translation & language detection
├── tts_module.py        # Text-to-speech with multi-language support
├── speech.py            # Speech recognition for user input
├── credentials.py       # Google Cloud authentication management
├── config.py            # Environment configuration
├── logger_utils.py      # Logging utilities
└── .env                 # Environment variables
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Webcam/Camera
- Google Cloud Platform account with enabled APIs:
  - Vision API
  - Translate API
  - Text-to-Speech API
  - Gemini AI API

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/parikshittalaviya/glassLingua.git
   cd glassLingua
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLO v3 files**
   - Download `yolov3.weights`, `yolov3.cfg`, and `coco.names`
   - Place them in your project directory
   - Update paths in `vision.py`

4. **Setup Google Cloud credentials**
   - Create a service account in Google Cloud Console
   - Download the JSON credentials file
   - Update the path in `credentials.py`

5. **Configure environment**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key" > .env
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

## 💡 How It Works

### Workflow Overview

1. **📷 Image Capture**: User captures book image via webcam
2. **🔍 Book Detection**: YOLO validates complete book presence
3. **📝 Text Extraction**: Google Vision API extracts text from book
4. **🤖 Text Enhancement**: Gemini AI refines and corrects extracted text
5. **🎤 Language Selection**: User speaks desired target language
6. **🌐 Translation**: Google Translate converts text to target language
7. **🔊 Audio Output**: Text-to-speech provides audio in selected language

### Key Components

#### Vision Module (`vision.py`)
- **YOLO Integration**: Detects books with 73-class object detection
- **Quality Validation**: Ensures complete book visibility (not partial)
- **Image Processing**: Handles camera feed and image preprocessing

#### OCR Module (`ocr_module.py`)
- **Google Vision API**: High-accuracy text recognition
- **Gemini Enhancement**: AI-powered text correction and formatting
- **Error Handling**: Robust error management for API failures

#### Translation System (`translation.py`)
- **Speech Recognition**: Voice-based language selection
- **Smart Detection**: Automatic language identification from speech
- **Multi-language Support**: Comprehensive Indian language coverage

#### TTS Module (`tts_module.py`)
- **Native Voice Support**: Language-specific voice models
- **Audio Management**: Efficient audio playback and cleanup
- **Quality Voices**: Uses Google's Wavenet voices for natural speech

## 🎮 Usage Guide

### Basic Operation

1. **Start Application**
   ```bash
   python main.py
   ```

2. **Capture Book Image**
   - Position book clearly in camera frame
   - Press any key to capture (avoid partial book views)
   - Press 'q' to exit

3. **Select Target Language**
   - Speak your desired language when prompted
   - Example: "I want Hindi" or "Translate to Gujarati"

4. **Listen to Translation**
   - Audio output will play automatically
   - Text is also displayed in console

### Tips for Best Results

- **📖 Book Positioning**: Ensure entire book is visible in frame
- **💡 Good Lighting**: Adequate lighting improves OCR accuracy
- **🎯 Clear Speech**: Speak clearly when selecting language
- **📱 Stable Camera**: Keep camera steady during capture

## 🛠️ Technical Details

### Dependencies

```python
# Core Libraries
opencv-python        # Computer vision and camera handling
numpy               # Numerical operations
pygame              # Audio playback

# Google Cloud APIs
google-cloud-vision      # OCR text extraction
google-cloud-translate   # Multi-language translation
google-cloud-texttospeech # Voice synthesis
google-generativeai      # Gemini AI integration

# Utilities
python-dotenv       # Environment management
html               # HTML entity handling
```

### Configuration Files

#### Environment Variables (`.env`)
```env
GROQ_API_KEY=your_groq_api_key_here
```

#### YOLO Configuration
Update paths in `vision.py`:
```python
weights_path = "path/to/yolov3.weights"
config_path = "path/to/yolov3.cfg" 
labels_path = "path/to/coco.names"
```

## 🔧 Customization

### Adding New Languages

1. **Update Language Map** (`translation.py`):
   ```python
   language_map = {
       "your_language": "language_code",
       # existing languages...
   }
   ```

2. **Add TTS Voice** (`tts_module.py`):
   ```python
   voice_mapping = {
       "language_code": texttospeech.VoiceSelectionParams(
           language_code="lang-REGION",
           ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
           name="voice-name"
       ),
   }
   ```

### Performance Optimization

- **YOLO Confidence**: Adjust detection threshold in `vision.py`
- **Image Resolution**: Modify resize parameters for speed vs accuracy
- **Cache Credentials**: Credentials are cached to reduce API calls

## 🎯 Use Cases

### Accessibility
- **Visual Impairment**: Audio book reading assistance
- **Learning Disabilities**: Text-to-speech support for reading
- **Mobility Limitations**: Hands-free book interaction

### Education
- **Language Learning**: Hear pronunciation in target languages
- **Multilingual Education**: Quick translation for study materials
- **Research**: Rapid content translation and audio consumption

### Professional
- **Content Creation**: Quick audio content from books
- **Translation Services**: Efficient book translation workflows
- **Documentation**: Audio documentation from printed materials

## 🔍 Troubleshooting

### Common Issues

#### Book Detection Problems
```
Issue: "No Book Detected" or "Partial Book Detected"
Solution: 
- Ensure entire book is in frame
- Improve lighting conditions
- Check YOLO model files are correctly placed
```

#### API Authentication Errors
```
Issue: Google Cloud API authentication failures
Solution:
- Verify service account credentials
- Check API enablement in Google Cloud Console
- Ensure correct file paths in credentials.py
```

#### Audio Playback Issues
```
Issue: No audio output or audio errors
Solution:
- Check pygame installation
- Verify system audio settings
- Ensure output directory exists and is writable
```

### Performance Optimization

- **Reduce Image Size**: Lower resolution for faster processing
- **Optimize YOLO**: Use smaller YOLO models for speed
- **Cache Management**: Clear temporary files regularly

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🍴 Fork the repository**
2. **🌟 Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **💻 Make your changes**
4. **✅ Test thoroughly**
5. **📝 Commit changes** (`git commit -m 'Add amazing feature'`)
6. **🚀 Push to branch** (`git push origin feature/amazing-feature`)
7. **🔄 Open a Pull Request**

### Areas for Contribution

- 🌐 Additional language support
- 🎯 Improved detection algorithms
- 🎨 GUI interface development
- 📱 Mobile app version
- 🔧 Performance optimizations
- 📚 Documentation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud Platform** for AI/ML APIs
- **YOLO** for object detection capabilities
- **OpenCV** community for computer vision tools
- **Python** ecosystem for robust libraries

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/parikshittalaviya/glassLingua/issues)
- **Discussions**: [Community discussions and help](https://github.com/parikshittalaviya/glassLingua/discussions)

---

**Made with ❤️ for accessibility and multilingual communication**

*glassLingua - Bridging languages through vision and voice*
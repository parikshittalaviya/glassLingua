import io
from google.cloud import vision
import google.generativeai as genai

from credentials import get_credentials
from tts_module import speak

def load_vision_client():
    """Loads Google Cloud Vision API client."""
    credentials = get_credentials()
    return vision.ImageAnnotatorClient(credentials=credentials)

def extract_text(vision_client):
    """Extracts text from an image using Google Cloud Vision API."""
    with io.open(r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\images\temp_images\temp.jpg", 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        speak(f'Google Vision Error has occurred')
        raise Exception(f'Google Vision Error occurred: {response.error.message}')

    detected_text = texts[0].description if texts else ''
    return ' '.join(detected_text.split())

def enhance_text_with_gemini(extracted_text):
    """Enhances extracted text using Google Cloud Gemini API."""

    # Load credentials
    credentials = get_credentials()
    
    # Configure Gemini API
    genai.configure(credentials=credentials)
    
    # Create a model instance
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Define the prompt for text refinement
    prompt = (
        f"Refine and correct the following text while keeping its original intent intact: "
        f"\n\n{extracted_text}\n\n"
        "Provide only the refined text without any additional description or heading."
    )
    
    # Get response from Gemini API
    response = model.generate_content(prompt)
    
    # Extract refined text
    enhanced_text = response.text.strip()
    
    return enhanced_text

import cv2
import numpy as np
import os
import json
import io
import time
import pygame
import speech_recognition as sr
from google.oauth2 import service_account
from groq import Groq
from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import html
import google.generativeai as genai

GROQ_API_KEY = "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"

def speak(text):
    """Converts text to speech, plays the audio, and ensures it's closed before proceeding."""
    
    # Load Text-to-Speech client
    tts_client = load_tts_client()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select voice
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-GB-Wavenet-F"
    )

    # Configure audio format
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Generate speech
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the file
    output_file = "output.mp3"
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    
    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.music.unload()  # Unload the file to free resources
    os.remove(output_file)  # Delete the file after playing to avoid permission issues

def capture_image():
    """Captures an image from the webcam."""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            speak("Failed to grab frame")
            break
        
        cv2.imshow("Press any key to capture (Press 'q' to e)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None  # Return None when 'q' is pressed to exit

        if key != 255:  # Any key other than 'q' is pressed
            image = frame.copy()
            cv2.imwrite("temp.jpg", image)
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return image

def load_vision_client():
    """Loads Google Cloud Vision API client."""
    with open(r"C:\Users\parik\Desktop\Glass Lingua\Google Cloud\googleToken.json") as source:
        info = json.load(source)
        credentials = service_account.Credentials.from_service_account_info(info)
    return vision.ImageAnnotatorClient(credentials=credentials)

def extract_text(vision_client):
    """Extracts text from an image using Google Cloud Vision API."""
    with io.open("temp.jpg", 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    
    if response.error.message:
        raise Exception(f'Google Vision Error occurred: {response.error.message}')
    
    detected_text = texts[0].description if texts else ''
    return ' '.join(detected_text.split())

def enhance_text_with_gemini(extracted_text):
    """Enhances extracted text using Google Cloud Gemini API."""
    # Set the environment variable for authentication (again if needed)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/parikshit/Desktop/googleToken.json"
    
    # Configure Gemini API
    # genai.configure(credentials=os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    genai.configure(api_key="abcd_api")
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

def speech_to_text_from_mic():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nListening... Please speak now.")
        speak("Listening... Please speak now.")

        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
            print("Processing your speech...")
            speak("Processing your speech...")
            
            audio_path = "captured_audio.wav"
            with open(audio_path, "wb") as f:
                f.write(audio.get_wav_data())
            
            return speech_to_text(audio_path)
        
        except sr.UnknownValueError:
            print("Error: Could not understand the audio.")
            speak("Sorry, I could not understand your audio. Please try again.")
            return ""
        
        except sr.RequestError as e:
            print(f"Error: Could not request results; {e}")
            speak("Sorry, I could not process your audio. Please try again.")
            return ""

def speech_to_text(audio_path):
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3-turbo",
            response_format="json",
            temperature=0.0
        )

    return transcription.text

def detect_language(user_input):
    """Detects the language mentioned in the user's input."""
    supported_languages = ["hindi", "gujarati", "english", "punjabi"]

    user_input = user_input.lower()  # Convert to lowercase for better matching
    for lang in supported_languages:
        if lang in user_input:
            return lang  # Return the detected language

    return None  # Return None if no language is detected

def get_language_from_user():
    """Continuously asks for user input until a valid language is detected."""
    while True:
        user_audio_text = speech_to_text_from_mic()
        print("\nUser's Audio Input:", user_audio_text)
        # speak(f"You said: {user_audio_text}")

        # Detect language
        language = detect_language(user_audio_text)

        if language:
            print(f"\nDetected Language: {language}")
            speak(f"Detected language is {language}")
            return language  # Return detected language and proceed
        else:
            print("\nNo language detected. Please specify a language.")
            speak("No language detected. Please specify a language.")

def load_translate_client():
    """Loads Google Cloud Translate API client."""  
    with open(r"C:\Users\parik\Desktop\Glass Lingua\Google Cloud\googleToken.json") as source:
        info = json.load(source)
        credentials = service_account.Credentials.from_service_account_info(info)
    
    return translate.Client(credentials=credentials)

def translate_text(client, text, target_language):
    """Translates text into the specified language using Google Cloud Translate."""
    result = client.translate(text, target_language=target_language)

    # return result["translatedText"]
    # Decode HTML entities to get normal quotation marks
    return html.unescape(result["translatedText"])

def load_tts_client():
    """Loads Google Cloud Text-to-Speech API client."""
    with open(r"C:\Users\parik\Desktop\Glass Lingua\Google Cloud\googleToken.json") as source:
        info = json.load(source)
        credentials = service_account.Credentials.from_service_account_info(info)
    return texttospeech.TextToSpeechClient(credentials=credentials)

def text_to_speech(tts_client, text, target_lang, output_file="final_output.mp3"):
    """Converts text to speech in the appropriate language and saves as an MP3 file."""
    
    # Voice selection based on target language
    voice_mapping = {
        "en": texttospeech.VoiceSelectionParams(language_code="en-GB", 
                                                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
                                                name="en-GB-Wavenet-F"),

        "hi": texttospeech.VoiceSelectionParams(language_code="hi-IN", 
                                                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
                                                name="hi-IN-Wavenet-F"),

        "gu": texttospeech.VoiceSelectionParams(language_code="gu-IN", 
                                                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
                                                name="gu-IN-Wavenet-D"),

        "pa": texttospeech.VoiceSelectionParams(language_code="pa-IN", 
                                                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
                                                name="pa-IN-Standard-A")
    }

    # Default to English if language not found
    selected_voice = voice_mapping.get(target_lang, voice_mapping["en"])

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure audio format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Generate speech
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=selected_voice,
        audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    print(f"Speech saved as {output_file}")
    
    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.music.unload()  # Unload the file to free resources
    os.remove(output_file)  # Delete the file after playing to avoid permission issues

def main():
    speak("Press any key to capture the image or press 'q' to exit.")
    
    while True:
        # Image Capturing
        image = capture_image()

        if image is None:  # If 'q' was pressed, terminate the program
            print("Exiting...")
            speak("Exiting program... Goodbye!")
            return
        else:
            break
    vision_client = load_vision_client()

    # Text Extraction
    extracted_text = extract_text(vision_client)
    print("\nExtracted Text:", extracted_text) 

    # Enhance the extracted text
    enhanced_text = enhance_text_with_gemini(extracted_text)
    print("\nEnhanced Text:", enhanced_text)

    # Get language from user
    language = get_language_from_user()

    # Map user-friendly language names to Google Translate codes
    language_map = {
        "hindi": "hi",
        "gujarati": "gu",
        "english": "en",
        "punjabi": "pa"
    }

    # Finding target language
    target_lang = language_map.get(language, "hi")  # Default to Hindi if not found

    # Load Translate Client once
    translate_client = load_translate_client()

    # Translate text
    translated_text = translate_text(translate_client, enhanced_text, target_lang)
    print("\nTranslated Text:", translated_text)

    # Load Text-to-Speech client
    tts_client = load_tts_client()

    # Convert translated text to speech
    text_to_speech(tts_client, translated_text, target_lang)

if __name__ == "__main__":

    main()

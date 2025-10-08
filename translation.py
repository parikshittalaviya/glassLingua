import html
from credentials import get_credentials
from google.cloud import translate_v2 as translate
from speech import speech_to_text_from_mic
from tts_module import speak

def detect_language(user_input):
    """Detects the language mentioned in the user's input."""
    supported_languages = [
        "hindi", "gujarati", "english", "punjabi", "bengali", "kannada", "marathi", "tamil", "telugu"
    ]
    
    user_input = user_input.lower()
    for lang in supported_languages:
        if lang in user_input:
            return lang
    return None

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
            return language
        else:
            print("\nNo language detected. Please specify a language.")
            speak("No language detected. Please specify a language.")

def load_translate_client():
    """Loads Google Cloud Translate API client."""
    credentials = get_credentials()
    return translate.Client(credentials=credentials)

def translate_text(client, text, target_language):
    """Translates text into the specified language using Google Cloud Translate."""
    result = client.translate(text, target_language=target_language)
    
    # Decode HTML entities to get normal quotation marks
    return html.unescape(result["translatedText"])

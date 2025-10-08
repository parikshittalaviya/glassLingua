import cv2

from vision import load_yolo, capture_image, detect_book
from ocr_module import load_vision_client, extract_text, enhance_text_with_gemini
from translation import load_translate_client, translate_text, get_language_from_user
from tts_module import load_tts_client, text_to_speech, speak

def main():
    # Load YOLO model and its parameters
    net, output_layers, _ = load_yolo()
    # Load the Vision client for OCR
    vision_client = load_vision_client()

    speak("Press any key to capture the image or press 'q' to exit.")

    while True:
        # Capture image from webcam
        image = capture_image()

        # If 'q' was pressed, image is None, so exit the program
        if image is None:
            print("Exiting...")
            speak("Exiting program... Goodbye!")
            return
        
        # Resize image for better detection accuracy
        resized_image = cv2.resize(image, (640, 640))

        # Book Detection
        processed_image = detect_book(resized_image, net, output_layers)
        
        if processed_image is not None:
            break  # Exit loop when a full book is detected
        else:
            print("No valid book detected. Retrying...\n")

    # Text Extraction
    extracted_text = extract_text(vision_client)
    print("\nExtracted Text:", extracted_text)

    # Enhance the extracted text
    enhanced_text = enhance_text_with_gemini(extracted_text)
    print("\nEnhanced Text:", enhanced_text)

    # Get language from the user
    language = get_language_from_user()

    # Map language names to Google Translate language codes
    language_map = {
        "hindi": "hi",
        "gujarati": "gu",
        "english": "en",
        "punjabi": "pa",
        "bengali": "bn-IN",
        "kannada": "kn-IN",
        "marathi": "mr-IN",
        "tamil": "ta-IN",
        "telugu": "te-IN"
    }

    # Finding target language code
    target_lang = language_map.get(language, "hi")

    # Load Translate Client
    translate_client = load_translate_client()

    # Translate text
    translated_text = translate_text(translate_client, enhanced_text, target_lang)
    print("\nTranslated Text:", translated_text)

    # Load Text-to-Speech client
    tts_client = load_tts_client()

    # Convert the translated text to speech and play it
    text_to_speech(tts_client, translated_text, target_lang)

if __name__ == "__main__":
    main()

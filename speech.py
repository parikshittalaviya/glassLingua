import speech_recognition as sr
import keyboard
from groq import Groq
from config import GROQ_API_KEY
from tts_module import speak

def speech_to_text_from_mic():
    recognizer = sr.Recognizer()

    print("\nPress 'r' to start recording...")
    speak("Press 'r' to start recording...")
    keyboard.wait('r')  # Wait until the user presses 'r'
    
    with sr.Microphone() as source:
        print("\nListening... Please speak now.")
        speak("Listening... Please speak now.")

        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
            print("Processing your speech...")
            speak("Processing your speech...")
            
            audio_path = r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\sounds\captured_audio.wav"
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

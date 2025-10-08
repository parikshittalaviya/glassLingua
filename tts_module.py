import os
import time
import json
import pygame
from google.cloud import texttospeech
from logger_utils import suppress_pygame_logs, restore_logs
from credentials import get_credentials

def play_audio(file_path):
    """Plays the audio file, waits for it to finish, unloads it, and then deletes the file."""
    # Suppress Pygame logs
    suppress_pygame_logs()

    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Restore logs after initializing pygame
    restore_logs()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.2)

    pygame.mixer.music.unload()  # Free resources
    os.remove(file_path)         # Delete file after playback

def load_tts_client():
    """Loads Google Cloud Text-to-Speech API client."""
    credentials = get_credentials()
    return texttospeech.TextToSpeechClient(credentials=credentials)

def speak(text):
    """Converts text to speech, plays the audio, and ensures it's closed before proceeding."""
    # Load Text-to-Speech client
    tts_client = load_tts_client()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select voice (English)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-GB-Wavenet-F"
    )

    # Configure audio format
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Generate speech
    response = tts_client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    # Save the generated audio
    output_file = "output.mp3"
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    # Play the audio using the helper function
    play_audio(output_file)

def text_to_speech(tts_client, text, 
                   target_lang, 
                   output_file=r"C:\Users\parik\Desktop\Glass Lingua\07_class_version\sounds\output.mp3"):
    """Converts text to speech in the appropriate language and saves as an MP3 file."""
    
    # Voice selection based on target language
    voice_mapping = {
        "en": texttospeech.VoiceSelectionParams(
            language_code="en-GB", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="en-GB-Wavenet-F"
        ),

        "hi": texttospeech.VoiceSelectionParams(
            language_code="hi-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="hi-IN-Wavenet-F"
        ),

        "gu": texttospeech.VoiceSelectionParams(
            language_code="gu-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="gu-IN-Wavenet-D"
        ),

        "pa": texttospeech.VoiceSelectionParams(
            language_code="pa-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="pa-IN-Standard-A"
        ),

        "bn": texttospeech.VoiceSelectionParams(
            language_code="bn-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="bn-IN-Wavenet-A"
        ),

        "kn": texttospeech.VoiceSelectionParams(
            language_code="kn-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="kn-IN-Wavenet-A"
        ),

        "mr": texttospeech.VoiceSelectionParams(
            language_code="mr-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="mr-IN-Wavenet-A"
        ),

        "ta": texttospeech.VoiceSelectionParams(
            language_code="ta-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="ta-IN-Wavenet-A"
        ),

        "te": texttospeech.VoiceSelectionParams(
            language_code="te-IN", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL, 
            name="te-IN-Wavenet-A"
        )
    }

    # Default to English if target language is not in the mapping
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

    # Save the generated audio
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    print(f"Speech saved as {output_file}")

    # Play the audio using the helper function
    play_audio(output_file)

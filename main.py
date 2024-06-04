# pip install SpeechRecognition
# pip install pip3 install googletrans==3.1.0a0
# pip install gtts
# pip install --update wheel
# pip install playsound

# mic driver issue on debain based distros:
# sudo apt-get install jackd2

# if pyaudio fails on Debian based distros follow:
# sudo apt-get install python3-dev
# sudo apt-get install portaudio19-dev
# sudo apt-get install python3-pyaudio


import speech_recognition as sr
import googletrans
from gtts import gTTS
from tempfile import NamedTemporaryFile
from playsound import playsound
import subprocess
import time

translator = googletrans.Translator()

from speech_indexing import extract_translation_info

def recordInput(src_lang, supported_languages):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        playsound('./audio_files/listening.mp3')
        audio = r.listen(source)

    try:
        # speak recognizing
        text = r.recognize_google(audio, language = src_lang)
        print(f"Input: {text}")
        nlp_op = extract_translation_info(text, supported_languages)
        return nlp_op
    
    except Exception as e:
        # speak say that again please
        print(f"Error: {e}")
        return "None"

def translateText(text, tgt_lang):
    tgt_out = translator.translate(text, dest=tgt_lang)
    print(f"Output: {tgt_out.text}")

    return tgt_out.text

def speak(text, tgt_lang):
    tts = gTTS(text=text, lang=tgt_lang)
    tts.save('./speech.mp3')
    time.sleep(4) # Depends on the system's performance
    playsound('./speech.mp3')

def process():
    pass

if __name__ == "__main__":
    
        supported_languages = {"hindi":"hi", "marathi":"mr", "gujarati":"gu", "kannada": "kn", "malayalam":"ml", "spanish":"es", }

        nlp_op = recordInput("en-in", supported_languages)
        print (nlp_op)
        if nlp_op["translate_index"] != None:
            if(nlp_op["language"] in supported_languages):
                print("en-in", supported_languages[nlp_op["language"]])
                tgt_out = translateText(nlp_op["text_to_translate"], supported_languages[nlp_op["language"]])
                speak(tgt_out, supported_languages[nlp_op["language"]])
            else:
                print('Try Saying "Translate I am going to school in Hindi"')
                playsound('./audio_files/error1.mp3')
                playsound('./audio_files/suggestion1.mp3')

        else:
            print('Try Saying "Translate I am going to school in Hindi"')
            playsound('./audio_files/error1.mp3')
            playsound('./audio_files/suggestion1.mp3')

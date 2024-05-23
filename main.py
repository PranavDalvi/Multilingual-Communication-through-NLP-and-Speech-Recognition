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

translator = googletrans.Translator()

from speech_indexing import extract_translation_info

def recordInput(src_lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # speak listening
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # speak recognizing
        text = r.recognize_google(audio, language = src_lang)
        print(f"Input: {text}")
        nlp_op = extract_translation_info(text)
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
    playsound('./speech.mp3')

if __name__ == "__main__":
    
        conv2keyword = {"Hindi":"hi"}

        nlp_op = recordInput("en-in")
        if(nlp_op["language"] in conv2keyword):
            print("en-in", conv2keyword[nlp_op["language"]])
            tgt_out = translateText(nlp_op["text_to_translate"], conv2keyword[nlp_op["language"]])
            speak(tgt_out, conv2keyword[nlp_op["language"]])
        else:
            print("Something went wrong please try again")

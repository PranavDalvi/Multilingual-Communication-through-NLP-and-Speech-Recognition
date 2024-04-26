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
        return text
    
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

def lang_selection(input):
    selector = {
        1:"mr",
        2:"hi",
        3:"en",
    }
    return selector.get(input, "None")

def speech_lang_selection(input):
    selector = {
        1:"mr-in",
        2:"hi-in",
        3:"en-in",
    }
    return selector.get(input, "None")

if __name__ == "__main__":
    
    src_lang = int(input("Enter Source Language: \n1. Marathi\n2. Hindi\n3. English\n"))
    tgt_lang = int(input("Enter Translation Language: \n1. Marathi\n2. Hindi\n3. English\n"))
    

    if src_lang == "None" or tgt_lang == "None":
        # speak
        print("Please Select Valid Option")
    else:
        src_lang = speech_lang_selection(src_lang)
        tgt_lang = lang_selection(tgt_lang)
        print(src_lang, tgt_lang)
        text = recordInput(src_lang)
        tgt_out = translateText(text, tgt_lang)
        speak(tgt_out, tgt_lang)
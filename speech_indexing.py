import spacy
import re
nlp = spacy.load("en_core_web_sm")


def detect_language(text):
    supported_languages = ["marathi", "hindi", "french", "spanish", "german", "italian", "portuguese", "japanese", "korean", "russian", "arabic"]
    for language in supported_languages:
        if language in text.lower():
            return language.capitalize()
    return None

def clean_text(text, language):
    text = re.sub(rf'\b(?:translate|convert|translation)\b.*\b(into|to)\s+{language}\b', '', text, flags=re.IGNORECASE)
    text = re.sub(rf'\b(into|to)\s+{language}\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(this sentence|of following sentence)\b', '', text, flags=re.IGNORECASE)
    return text

def extract_translation_info(sentence):
    doc = nlp(sentence)
    translate_index = None
    for token in doc:
        if token.lemma_ == "translate" or token.lemma_ == "convert" or token.lemma_ == "translation":
            translate_index = token.i
            break


    language = detect_language(sentence)
    if translate_index is not None and translate_index + 1 < len(doc):
        command = "Translate"
        
        text_to_translate = ""
        for token in doc[translate_index + 1:]:
            text_to_translate += token.text + " "
    else:
        text_to_translate = ''

    text_to_translate = clean_text(text_to_translate, language)

    return {
        'command': command,
        'language': language,
        'text_to_translate': text_to_translate.strip()
    }

# Testing examples
sentences = [
    "Please translate this sentence into Hindi In C language pointers serve as references to other variables, akin to person A pointing to person B",
    "Translate this sentence into Hindi Pointers in C language function as references to other variables, much like person A indicating person B",
    "Could you translate this sentence into Hindi Pointers within C programming act as references to other variables resembling person A gesturing towards person B",
    "I'd like this sentence translated into Hindi The pointers in C language represent references to other variables similar to person A pointing towards person B",
    "Kindly translate this sentence into Hindi Pointers in C resemble person A pointing to person B as they reference other variables",
    "Translate I am going to school into French",
    "Translate Hello to Hindi",
    "Please do translation of following sentence into hindi In Chekki programming pointers are akin to person A pointing towards person B referencing other variables",
    "Would you translate this sentence into Hindi In C programming pointers are akin to person A pointing towards person B referencing other variables",
]

translations = [extract_translation_info(sentence) for sentence in sentences]

for index, translation in enumerate(translations):
    print(f"Example {index + 1}:")
    print(f"  Command: {translation['command']}")
    print(f"  Target Language: {translation['language']}")
    print(f"  Text to Translate: {translation['text_to_translate']}")

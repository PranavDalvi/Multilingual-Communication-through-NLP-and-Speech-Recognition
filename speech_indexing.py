import spacy
import re
nlp = spacy.load("en_core_web_sm")


def detect_language(text, supported_languages):
    for key, value  in supported_languages.items():
        print(f"Key: {key}")
        if key in text.lower():
            return key.lower()
    return None

def clean_text(text, language):
    text = re.sub(rf"\b(?:translate|convert|translation)\b.*\b(into|to)\s+{language}\b", "", text, flags=re.IGNORECASE)
    text = re.sub(rf"\b(into|to)\s+{language}\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(this sentence|of following sentence)\b", "", text, flags=re.IGNORECASE)
    return text

def extract_translation_info(sentence, supported_languages):
    doc = nlp(sentence)
    translate_index = None
    for token in doc:
        if token.lemma_ == "translate" or token.lemma_ == "convert" or token.lemma_ == "translation":
            translate_index = token.i
            break

    language = detect_language(sentence, supported_languages)
    if translate_index is not None and translate_index + 1 < len(doc):
        text_to_translate = ""
        for token in doc[translate_index + 1:]:
            text_to_translate += token.text + " "
    else:
        text_to_translate = ""

    text_to_translate = clean_text(text_to_translate, language)

    return {
        "translate_index" : translate_index,
        "language": language,
        "text_to_translate": text_to_translate.strip()
    }

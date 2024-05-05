import spacy
def extract_input(input_string):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(input_string)
    lang = doc.lang_

    sentence = None
    tgt_lang= None

    for token in doc:
        if token.text.lower() in ["translate", "convert"]:
            sentence = doc[token.i + 1:].text.strip()
            break

    # for ent in doc.ents:
    #     if ent.label_ in ["language", "into"]:
    #         tgt_lang = ent.text.lower()
    #         break


    for token in doc:
        if token.text.lower() in ["to", "into"]:
            tgt_lang_candidate = doc[token.i+1]
            if tgt_lang_candidate.pos_ in ["PROPN", "ADJ"]:
                tgt_lang = tgt_lang_candidate.text.lower()
                replacer =f"{doc[token.i]} {doc[token.i+1]}"
                print(replacer)
                break
    
    sentence1 = sentence.replace(replacer, "")
    
    return sentence1, tgt_lang

sentence1, tgt_lang1 = extract_input("Translate this sentence into hindi So the pointers in C language are reference to some other variable. It is same as person A pointing to person B")

print(f"Sentence 1: {sentence1}, Target language 1: {tgt_lang1}")
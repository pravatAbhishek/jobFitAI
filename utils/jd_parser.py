import spacy


nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_jd(jd_text):
    doc = nlp(jd_text.lower())
    keywords = [chunk.text.strip() for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
    return list(set(keywords))

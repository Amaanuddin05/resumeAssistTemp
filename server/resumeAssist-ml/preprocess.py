import spacy
import re
from nltk.corpus import stopwords
from nltk import download

# Download NLTK stopwords (only once)
download('stopwords')

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def clean_and_lemmatize(text):
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if token.is_alpha and token.lemma_ not in stop_words and not token.is_stop
    ]
    return ' '.join(tokens)

def extract_skills(text):
    doc = nlp(text)
    skills = set()
    
    # Extract noun chunks (good for skills like "machine learning", "cloud computing")
    for chunk in doc.noun_chunks:
        if 1 <= len(chunk.text.split()) <= 3:  # Filter too-long chunks
            skills.add(chunk.text.lower())
    
    # Add named entities labeled as skills (optional, not all are skills)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "SKILL"]:
            skills.add(ent.text.lower())

    return list(skills)

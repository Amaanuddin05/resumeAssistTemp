from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
from preprocess import clean_and_lemmatize, extract_skills


def get_ats_score(resume, jd):
    if not resume.strip() or not jd.strip():
        return 0
    try:
        tfidf = TfidfVectorizer().fit_transform([resume, jd])
        return round(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100)
    except:
        return 0

def get_keyword_match(resume, jd):
    resume = clean_and_lemmatize(resume)
    jd = clean_and_lemmatize(jd)
    
    resume_words = set(resume.split())
    jd_words = set(jd.split())
    match = resume_words.intersection(jd_words)
    
    return round(len(match) / len(jd_words) * 100) if jd_words else 0


def get_readability(resume):
    score = textstat.flesch_reading_ease(resume)
    if score > 60:
        return "Good"
    elif score > 30:
        return "Average"
    else:
        return "Poor"

import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat


def get_ats_score(resume, jd):
    if not resume.strip() or not jd.strip():
        return 0
    try:
        tfidf = TfidfVectorizer().fit_transform([resume, jd])
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(score * 100)
    except ValueError:
        # Happens if inputs are only stop words
        return 0

def get_keyword_match(resume, jd):
    resume_words = set(resume.lower().split())
    jd_words = set(jd.lower().split())
    if not jd_words:
        return 0
    match = resume_words.intersection(jd_words)
    return round(len(match) / len(jd_words) * 100)

def get_readability(resume):
    score = textstat.flesch_reading_ease(resume)
    if score > 60:
        return "Good"
    elif score > 30:
        return "Average"
    else:
        return "Poor"

if __name__ == "__main__":
    # Read two lines from stdin
    resume_text = sys.stdin.readline().strip()
    jd_text = sys.stdin.readline().strip()

    if not resume_text or not jd_text:
        print(json.dumps({
            "error": "Resume or Job Description text is empty"
        }))
        sys.exit(1)

    result = {
        "ats_score": get_ats_score(resume_text, jd_text),
        "keyword_match": get_keyword_match(resume_text, jd_text),
        "readability": get_readability(resume_text)
    }

    print(json.dumps(result))

import sys
import json
import re
import spacy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import download
from spacy.matcher import PhraseMatcher

# download('stopwords')

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

def load_skills_from_json(filepath="skills_all_merged.json"):
    with open(filepath, "r") as f:
        return [skill.lower() for skill in json.load(f)]

def extract_skills(text, skill_list):
    doc = nlp(text.lower())
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in skill_list]
    matcher.add("SKILLS", patterns)
    matches = matcher(doc)
    matched_skills = {doc[start:end].text.strip().lower() for _, start, end in matches}
    return sorted(matched_skills)

def extract_keywords(text):
    doc = nlp(text.lower())
    return {
        token.lemma_ for token in doc
        if token.pos_ in {"NOUN", "PROPN", "VERB", "ADJ"}
        and token.is_alpha
        and token.lemma_ not in stop_words
        and not token.is_stop
    }

def get_keyword_match(resume: str, jd: str):
    resume_keywords = extract_keywords(resume)
    jd_keywords = extract_keywords(jd)
    match = resume_keywords & jd_keywords
    return round(len(match) / len(jd_keywords) * 100) if jd_keywords else 0

def get_tfidf_similarity(text1: str, text2: str):
    if not text1.strip() or not text2.strip():
        return 0
    try:
        tfidf = TfidfVectorizer().fit_transform([text1, text2])
        return round(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100)
    except:
        return 0

def get_resume_score(skill_match, keyword_match, tfidf_score):
    return round(
        (skill_match * 0.5) +
        (keyword_match * 0.2) +
        (tfidf_score * 0.3)
    )

def main():
    data = json.loads(sys.stdin.read())
    resume_text = data.get("resume", "")
    jd_text = data.get("jd", "")

    if not resume_text or not jd_text:
        print(json.dumps({"error": "Missing input"}))
        sys.exit(1)

    skill_list = load_skills_from_json("skills_all_merged.json")
    resume_skills = extract_skills(resume_text, skill_list)
    jd_skills = extract_skills(jd_text, skill_list)
    matched_skills = list(set(resume_skills) & set(jd_skills))
    skill_match_score = round(len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0

    keyword_match = get_keyword_match(resume_text, jd_text)
    tfidf_score = get_tfidf_similarity(' '.join(resume_skills), ' '.join(jd_skills))

    resume_score = get_resume_score(skill_match_score, keyword_match, tfidf_score)

    result = {
        "resume_score": resume_score,
        "skill_match_score": skill_match_score,
        "keyword_match": keyword_match,
        "tfidf_score": tfidf_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()

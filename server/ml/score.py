import sys
import json
import re
import textstat
import spacy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import download
from spacy.matcher import PhraseMatcher

download('stopwords')

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words("english"))

COMMON_SKILLS = {
    'angular', 'tailwind css', 'bootstrap', 'html5', 'css3',
    'javascript', 'node.js', 'express.js', 'mongodb', 'mysql',
    'jwt authentication', 'restful apis', 'firebase', 'pwa',
    'python', 'java', 'c', 'git', 'ui/ux', 'postman'
}

def extract_skills(text, custom_skill_list=None):
    doc = nlp(text.lower())
    chunks = set([chunk.text.strip() for chunk in doc.noun_chunks])
    entities = set([ent.text.strip() for ent in doc.ents])
    raw_skills = chunks.union(entities)

    cleaned_skills = set()
    for phrase in raw_skills:
        if len(phrase) < 2 or phrase in {"i", "projects", "a focus", "the system"}:
            continue
        if not re.search(r'[a-zA-Z]', phrase):
            continue
        if len(phrase.split()) > 6:
            continue
        cleaned_skills.add(phrase)

    # Optional: add matched known tech skills from COMMON_SKILLS
    if custom_skill_list:
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        patterns = [nlp.make_doc(skill) for skill in custom_skill_list]
        matcher.add("TECH_SKILLS", patterns)
        matches = matcher(doc)
        known_matches = {doc[start:end].text for _, start, end in matches}
        cleaned_skills = cleaned_skills.union(known_matches)

    return sorted(cleaned_skills)

def clean_and_lemmatize(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    doc = nlp(text.lower())
    return ' '.join([
        token.lemma_ for token in doc
        if token.is_alpha and token.lemma_ not in stop_words and not token.is_stop
    ])

# def extract_skills(text):
#     doc = nlp(text)
#     skills = set()
#     for chunk in doc.noun_chunks:
#         if 1 <= len(chunk.text.split()) <= 3:
#             skills.add(chunk.text.lower())
#     for ent in doc.ents:
#         if ent.label_ in ["ORG", "PRODUCT", "SKILL"]:
#             skills.add(ent.text.lower())
#     return list(skills)

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
    match = resume_words & jd_words
    return round(len(match) / len(jd_words) * 100) if jd_words else 0

def get_readability(resume):
    score = textstat.flesch_reading_ease(resume)
    if score > 60:
        return "Good"
    elif score > 30:
        return "Average"
    return "Poor"

def main():
    data = json.loads(sys.stdin.read())
    resume_text = data.get("resume", "")
    jd_text = data.get("jd", "")


    if not resume_text or not jd_text:
        print(json.dumps({"error": "Missing input"}))
        sys.exit(1)

    resume_skills = extract_skills(resume_text, COMMON_SKILLS)
    jd_skills = extract_skills(jd_text, COMMON_SKILLS)
    matched_skills = list(set(resume_skills) & set(jd_skills))
    skill_match_score = round(len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0

    result = {
        "ats_score": get_ats_score(resume_text, jd_text),
        "keyword_match": get_keyword_match(resume_text, jd_text),
        "readability": get_readability(resume_text),
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "skill_match_score": skill_match_score
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()

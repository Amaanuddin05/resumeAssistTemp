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

def check_contact_info(text: str):
    email_found = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    phone_found = re.search(r"(\+91)?[-\s]?[6-9]\d{9}", text)
    name_found = re.search(r"(?i)^([A-Z][a-z]+(\s[A-Z][a-z]+)+)", text.strip().split("\n")[0])
    score = 0
    if email_found:
        score += 3.5
    if phone_found:
        score += 3.5
    if name_found:
        score += 3.0
    return round(score)

def check_education(text: str):
    education_keywords = [
        "b.tech", "bachelor of technology", "b.e", "m.tech", "m.e", 
        "b.sc", "m.sc", "mba", "phd", "bca", "mca"
    ]
    suggestions = []
    score = 100
    text_lower = text.lower()

    if not any(kw in text_lower for kw in education_keywords):
        suggestions.append("Missing or unclear degree information.")
    if not re.search(r"\b(20\d{2})\b", text_lower):
        suggestions.append("Missing education dates (e.g. 2022).")
    if not re.search(r"(\*|\-|\•)", text):
        suggestions.append("Consider formatting education entries with bullet points.")

    score -= len(suggestions) * 25
    score = max(score, 0)

    return int(round(score * 0.1)), suggestions

def check_experience(text: str):
    suggestions = []
    score = 100
    text_lower = text.lower()

    if not re.search(r"\b(20\d{2})\b", text_lower):
        suggestions.append("Missing dates in experience section.")
    if not re.search(r"(\*|\-|\•)", text):
        suggestions.append("Use bullet points to list responsibilities.")
    action_verbs = [
        "developed", "built", "created", "implemented", "led", "managed",
        "designed", "engineered", "optimized", "improved", "analyzed"
    ]
    if not any(verb in text_lower for verb in action_verbs):
        suggestions.append("Use strong action verbs to describe your work.")

    score -= len(suggestions) * 25
    score = max(score, 0)

    return int(round(score * 0.1)), suggestions

def get_resume_score(skill_score, contact_score, edu_score, exp_score, tfidf_score):
    return round(
        (skill_score / 100) * 30 +
        (contact_score / 10) * 10 +
        (edu_score / 10) * 15 +
        (exp_score / 10) * 15 +
        (tfidf_score / 100) * 30
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
    remaining_skills = list(set(jd_skills) - set(matched_skills))

    tfidf_score = get_tfidf_similarity(resume_text, jd_text)
    contact_score = check_contact_info(resume_text)
    edu_score, edu_suggestions = check_education(resume_text)
    exp_score, exp_suggestions = check_experience(resume_text)

    resume_score = get_resume_score(
        skill_match_score, contact_score, edu_score, exp_score, tfidf_score
    )

    result = {
        "resume_score": resume_score,
        "skill_match_score": skill_match_score,
        "tfidf_score": tfidf_score,
        "contact_score": contact_score,
        "education_score": edu_score,
        "experience_score": exp_score,
        "education_suggestions": edu_suggestions,
        "experience_suggestions": exp_suggestions,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "remaining_skills": remaining_skills
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()

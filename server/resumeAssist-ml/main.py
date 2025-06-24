from score import get_ats_score, get_keyword_match, get_readability
from preprocess import clean_and_lemmatize, extract_skills
import json

def load_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

resume_raw = load_text("sample_resume.txt")
jd_raw = load_text("sample_jd.txt")
print("\nRaw resume")
print(resume_raw)
print("\nJD raw")
print(jd_raw)


# === NLP Preprocessing ===
resume_clean = clean_and_lemmatize(resume_raw)
jd_clean = clean_and_lemmatize(jd_raw)

print("\n🧼 Cleaned & Lemmatized Resume:")
print(resume_clean)

print("\n🧼 Cleaned & Lemmatized JD:")
print(jd_clean)

# === Skill Extraction ===
resume_skills = extract_skills(resume_raw)
jd_skills = extract_skills(jd_raw)
matched_skills = set(resume_skills) & set(jd_skills)
skill_match_score = round(len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0



print("\n🧠 Extracted Resume Skills:")
print(resume_skills)

print("\n🎯 Extracted JD Skills:")
print(jd_skills)

print("\n✅ Matched Skills:")
print(matched_skills)

print(f"\n🎯 Skill Match Score: {skill_match_score}%")

# === Scoring ===
ats = get_ats_score(resume_raw, jd_raw)
keyword_match = get_keyword_match(resume_raw, jd_raw)
readability = get_readability(resume_raw)

print("\n📊 Final Scoring")
print(f"📄 ATS Score: {ats}%")
print(f"🔍 Keyword Match: {keyword_match}%")
print(f"📘 Readability: {readability}")



result = {
    "ats_score": ats,
    "keyword_match": keyword_match,
    "readability": readability,
    "resume_skills": resume_skills,
    "jd_skills": jd_skills,
    "matched_skills": list(matched_skills),
    "skill_match_score": skill_match_score
}

with open("report.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("\n✅ Results saved to report.json")
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Score Summary
scores = {
    "ATS Score": ats,
    "Keyword Match": keyword_match,
    "Skill Match": skill_match_score
}

plt.figure(figsize=(8, 5))
sns.barplot(x=list(scores.keys()), y=list(scores.values()), palette="muted")
plt.title("Resume vs Job Description Score Summary")
plt.ylabel("Score (%)")
plt.ylim(0, 100)
for i, v in enumerate(scores.values()):
    plt.text(i, v + 2, f"{v}%", ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig("score_summary.png")
plt.show()

from matplotlib_venn import venn2

plt.figure(figsize=(6,6))
venn2([set(resume_skills), set(jd_skills)], set_labels=("Resume Skills", "JD Skills"))
plt.title("Skill Overlap")
plt.savefig("skill_overlap.png")
plt.show()


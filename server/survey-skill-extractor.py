import pandas as pd
import json

# Load the CSV
df = pd.read_csv("survey_results_public.csv", low_memory=False)

# Define relevant tech skill columns
target_columns = [
    "LanguageHaveWorkedWith",
    "DatabaseHaveWorkedWith",
    "PlatformHaveWorkedWith",
    "WebframeHaveWorkedWith",
    "EmbeddedHaveWorkedWith",
    "MiscTechHaveWorkedWith",
    "ToolsTechHaveWorkedWith",
    "NEWCollabToolsHaveWorkedWith",
    "OfficeStackAsyncHaveWorkedWith",
    "OfficeStackSyncHaveWorkedWith",
    "AISearchDevHaveWorkedWith"
]

# Alias mapping
ALIASES = {
    "js": "javascript",
    "node": "node.js",
    "nodejs": "node.js",
    "py": "python",
    "gcp": "google cloud",
    "sql server": "microsoft sql server",
    ".net": "dotnet",
    "asp.net": "dotnet",
    "aws lambda": "aws",
    "azure functions": "azure",
    "postgres": "postgresql",
    "k8s": "kubernetes"
}

# Terms to ignore
BLACKLIST = {
    "none", "n/a", "na", "null", "no", "other",
    "don't know", "nothing", "not applicable",
    "prefer not to say", "none of the above"
}

# Helper function to clean and normalize
def clean_skill(skill: str) -> str:
    skill = skill.strip().lower()
    return ALIASES.get(skill, skill)

# Collect all valid skills
all_skills = []

for col in target_columns:
    if col in df.columns:
        for entry in df[col].dropna():
            for skill in str(entry).split(";"):
                skill = clean_skill(skill)
                if skill and skill not in BLACKLIST:
                    all_skills.append(skill)

# Deduplicate, sort, and save
unique_skills = sorted(set(all_skills))

with open("skills.json", "w") as f:
    json.dump(unique_skills, f, indent=2)

print(f"✅ Extracted {len(unique_skills)} cleaned and deduplicated skills to skills.json")

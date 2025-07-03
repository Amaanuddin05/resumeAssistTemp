import json

# Load the cleaned skill list
with open("skills_enriched1.json", "r") as f:
    original_skills = json.load(f)

# Normalize original
original_set = set(skill.lower().strip() for skill in original_skills)

# Add enriched extra skills
extra_skills = ["miro", "notion", "slack", "asana", "jira", "trello", "confluence", "monday.com",
"airtable", "figjam", "obsidian", "zoho crm", "salesforce lightning",
"hubspot forms", "firebase crashlytics", "tableau prep", "looker studio",
"power bi dashboards", "data storytelling", "kpi dashboards"

]

# Normalize and merge
extra_set = set(skill.lower().strip() for skill in extra_skills)
merged_skills = sorted(original_set | extra_set)  # Set union and sort

# Save to enriched file
with open("skills_enriched1.json", "w") as f:
    json.dump(merged_skills, f, indent=2)

print(f"✅ Enriched skill list saved with {len(merged_skills)} unique skills.")

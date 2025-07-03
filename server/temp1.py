import json
from collections import Counter

# File path to your categorized skill map
input_file = "skills_by_category.json"
output_file = "skill_category_counts.json"

# Load the skill-to-category mapping
with open(input_file, "r") as f:
    skills_by_category = json.load(f)

# Count how many times each category appears
category_counts = Counter(skills_by_category.values())

# Sort by descending frequency
sorted_counts = dict(sorted(category_counts.items(), key=lambda x: -x[1]))

# Print preview
print("🔢 Skill counts by category (top 10):")
for cat, count in list(sorted_counts.items())[:10]:
    print(f"{cat}: {count}")

# Save to JSON
with open(output_file, "w") as f:
    json.dump(sorted_counts, f, indent=2)

print(f"\n✅ Saved full category counts to '{output_file}'")

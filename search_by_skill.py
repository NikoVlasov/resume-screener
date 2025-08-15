import requests
from collections import defaultdict
import csv
from datetime import datetime

# ======================
# Settings
# ======================
BASE_URL = "http://127.0.0.1:8000/resumes"
HEADERS = {
    "Authorization": (
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzU1MTc5NjQ3fQ."
        "n4c0F9LEqiUYrYT_QmgP-QLhX3dbMETMae95RSgY9To"
    )
}

skills_to_search = ["Python", "SQL", "Power BI"]
keywords_to_search = ["data analysis", "machine learning", "reporting"]

# ======================
# Functions
# ======================

def fetch_all_resumes():
    """Fetches all resumes from the server via API."""
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
        return []

def collect_resumes(skills, keywords):
    """Collects resumes that match given skills and keywords."""
    combined = defaultdict(lambda: {"skills": set(), "keywords": set()})
    resumes = fetch_all_resumes()

    for resume in resumes:
        filename = resume.get("filename") or resume.get("id", "No file name")
        parsed_data = resume.get("parsed_data", {})
        parsed_skills = parsed_data.get("skills", [])
        text = parsed_data.get("text", "").lower()

        # Normalize skills
        normalized_skills = []
        for s in parsed_skills:
            if isinstance(s, str):
                normalized_skills.append(s.lower())
            elif isinstance(s, dict):
                normalized_skills.append(s.get("skill", "").lower())
                if s.get("matched_alias"):
                    normalized_skills.append(s.get("matched_alias").lower())

        # Skills check
        for skill in skills:
            if skill.lower() in normalized_skills:
                combined[filename]["skills"].add(skill)

        # Keywords check
        for keyword in keywords:
            if keyword.lower() in text:
                combined[filename]["keywords"].add(keyword)

    return combined

def print_combined_resumes(combined_resumes):
    """Prints the found resumes."""
    if not combined_resumes:
        print("⚠ No resumes found with these skills or keywords.\n")
        return

    print("\n📄 Found resumes:\n")
    for filename, data in combined_resumes.items():
        skills_list = ", ".join(sorted(data["skills"])) or "None"
        keywords_list = ", ".join(sorted(data["keywords"])) or "None"
        print(f"✅ {filename}:")
        print(f"   - Skills: {skills_list}")
        print(f"   - Keywords: {keywords_list}\n")

def export_to_csv(combined_resumes, filename=None):
    """Exports results to CSV."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resumes_{timestamp}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Skills", "Keywords"])
        for file, data in combined_resumes.items():
            writer.writerow([
                file,
                ", ".join(sorted(data["skills"])),
                ", ".join(sorted(data["keywords"]))
            ])

    print(f"\n💾 Results exported to file: {filename}")
    return filename  # returns filename for later viewing

def show_csv(filename):
    """Displays CSV content in the console."""
    print(f"\n📊 Contents of {filename}:\n")
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

# ======================
# Main execution
# ======================
if __name__ == "__main__":
    combined_resumes = collect_resumes(skills_to_search, keywords_to_search)
    print_combined_resumes(combined_resumes)
    csv_file = export_to_csv(combined_resumes)
    show_csv(csv_file)

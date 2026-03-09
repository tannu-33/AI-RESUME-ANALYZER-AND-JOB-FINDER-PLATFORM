import json
import os


def load_roles():
    path = os.path.join("data", "job_roles.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def skill_gap(resume_text, selected_role):
    roles = load_roles()

    role_skills = roles[selected_role]["skills"]
    resume_text_lower = resume_text.lower()

    matched = []
    missing = []

    for skill in role_skills:
        if skill.lower() in resume_text_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    coverage = round((len(matched) / len(role_skills)) * 100, 2)

    return coverage, matched, missing

def learning_resources(skill):
    return {
        "YouTube": f"https://www.youtube.com/results?search_query=learn+{skill}",
        "Coursera": f"https://www.coursera.org/search?query={skill}",
        "Udemy": f"https://www.udemy.com/courses/search/?q={skill}",
        "GeeksforGeeks": f"https://www.geeksforgeeks.org/?s={skill}"
    }
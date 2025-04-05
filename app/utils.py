import re

def extract_name(text):
    lines = text.strip().split("\n")
    for line in lines:
        if line.strip() and line[0].isupper():
            return line.strip()
    return "Unknown"

def extract_email(text):
    match = re.search(r"[\\w\\.-]+@[\\w\\.-]+", text)
    return match.group(0) if match else "Not found"

def extract_phone(text):
    match = re.search(r"\\+?\\d?[\\s-]?(\\d{3}[\\s-]?\\d{3}[\\s-]?\\d{4})", text)
    return match.group(0) if match else "Not found"

def extract_skills(text, skill_list=None):
    if not skill_list:
        skill_list = ["python", "java", "sql", "excel", "machine learning", "nlp", "data analysis"]
    return list(set([skill for skill in skill_list if skill.lower() in text.lower()]))

def extract_education(text):
    education_keywords = ["bachelor", "master", "b.sc", "m.sc", "phd", "degree"]
    for line in text.lower().split("\\n"):
        if any(word in line for word in education_keywords):
            return line.strip().capitalize()
    return "Not found"

def extract_experience(text):
    experience_pattern = re.findall(r"(\\d+\\+? years|\\d+ years of experience)", text.lower())
    return experience_pattern[0] if experience_pattern else "Not found"

def extract_details(text):
    return {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Education": extract_education(text),
        "Experience": extract_experience(text),
        "Skills": ", ".join(extract_skills(text))
    }
def highlight_skills_in_text(text, skills):
    for skill in skills:
        regex = re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE)
        text = regex.sub(f"**:blue[{skill.upper()}]**", text)
    return text


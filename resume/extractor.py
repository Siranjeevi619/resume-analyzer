import re

SECTION_HEADER = {
    "summary":["summary", "profile", "objective"],
    "skills":["skills", "technical skills","skill set"],
    "experience" :["experience", "work experience", "employment"],
    "education" :["education", "knowledge", "academic", "academic profile"],
    "projects":["projects"]
}


def extract_section(text : str) -> dict:
    text_lower = text.lower()
    sections = {}
    for section , headers in SECTION_HEADER.items():
        for header in headers:
            pattern = rf"{header}[\s\S]*?(?=\n[A-Z][A-Za-z ]+:|\Z)"
            match = re.search(pattern, text_lower)
            if match:
                sections[section] = match.group().strip()
                break
    return sections

def extract_skills(text : str) -> list:
    keywords = ["python", "java", "spring", "react", "node",
        "mongodb", "sql", "docker", "aws", "software developer","git"]
    text_lower = text.lower()
    skills = ()
    for skill in keywords:
        if skill in text_lower:
            skills.__add__(skill)
    return sorted(set(skills))
from typing import List
from jd.analyzer import match_resume_with_jd

def calculate_skill_match(resume_skills: List[str], jd_text: str) -> float:
    jd_text = jd_text.lower()
    matched = [skill for skill in resume_skills if skill in jd_text]

    if not resume_skills:
        return 0.0

    return len(matched) / len(resume_skills)


def calculate_similarity_score(resume_text: str) -> float:
    results = match_resume_with_jd(resume_text)

    if not results:
        return 0.0

    avg_distance = sum(score for _, score in results) / len(results)

    similarity = max(0.0, 1 - avg_distance)
    return similarity


def calculate_completeness(sections: dict) -> float:
    filled = sum(1 for value in sections.values() if value)
    total = len(sections)
    return filled / total


def calculate_ats_score(
    resume_text: str,
    resume_skills: List[str],
    jd_text: str,
    sections: dict
) -> dict:

    skill_score = calculate_skill_match(resume_skills, jd_text)
    similarity_score = calculate_similarity_score(resume_text)
    completeness_score = calculate_completeness(sections)

    final_score = (
        skill_score * 40 +
        similarity_score * 40 +
        completeness_score * 20
    )

    return {
        "skill_match_percent": round(skill_score * 100, 2),
        "semantic_similarity_percent": round(similarity_score * 100, 2),
        "completeness_percent": round(completeness_score * 100, 2),
        "final_ats_score": round(final_score, 2)
    }

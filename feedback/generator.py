from feedback.prompts import RESUME_FEEDBACK_PROMPT
from llm.llm_client import implement_model

def generate_resume_feedback(
    resume_text: str,
    resume_skills: list,
    job_description: str,
    ats_result: dict
) -> dict:

    chat_model = implement_model()

    messages = RESUME_FEEDBACK_PROMPT.format_messages(
        job_description=job_description,
        resume_text=resume_text,
        resume_skills=", ".join(resume_skills),
        skill_match=ats_result["skill_match_percent"],
        semantic_similarity=ats_result["semantic_similarity_percent"],
        completeness=ats_result["completeness_percent"],
        final_score=ats_result["final_ats_score"]
    )

    response = chat_model.invoke(messages)

    return {
        "feedback": response.content
    }

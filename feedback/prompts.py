from langchain_core.prompts import ChatPromptTemplate

RESUME_FEEDBACK_PROMPT = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a senior HR interviewer and ATS expert. "
     "Do not invent experience. Be professional and precise."),
    
    ("human", """
Job Description:
{job_description}

Candidate Resume:
{resume_text}

Extracted Skills:
{resume_skills}

ATS Score Breakdown:
- Skill Match: {skill_match}%
- Semantic Similarity: {semantic_similarity}%
- Resume Completeness: {completeness}%
- Final ATS Score: {final_score}

Tasks:
1. List 3 strengths
2. List 3 weaknesses
3. Give 5 improvements
4. Rewrite one experience bullet
5. Give section-wise feedback
""")
])

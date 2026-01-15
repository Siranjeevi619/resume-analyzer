from langchain_core.prompts import ChatPromptTemplate

RESUME_CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are a professional resume reviewer and technical interviewer. "
     "Answer strictly based on the resume and job description. "
     "Do not invent experience."),
    
    ("human",
     """
Resume:
{resume_text}

Job Description:
{job_description}

Conversation History:
{chat_history}

User Question:
{question}
""")
])

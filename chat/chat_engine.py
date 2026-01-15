from chat.prompts import RESUME_CHAT_PROMPT
from chat.memory import get_memory
from llm.llm_client import implement_model

def resume_chat(session_id : str,
                resume_text: str,
                job_description:str ,
                question : str) -> str:
    memory = get_memory(session_id)
    chat_model = implement_model()
    message = RESUME_CHAT_PROMPT.format_messages(resume_text = resume_text, 
                                                 job_description = job_description,
                                                 chat_history = memory.buffer,
                                                 question = question)
    response = chat_model.invoke(message)
    memory.save_context(
    {"input": question},
    {"output": response.content}
    )

    
    return response.content
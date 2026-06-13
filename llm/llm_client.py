from langchain_groq import ChatGroq
import os

def implement_model():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=512,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

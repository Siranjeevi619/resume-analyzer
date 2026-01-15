from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os

def implement_model():
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        task="conversational",
        max_new_tokens=512,
        temperature=0.3,
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    return ChatHuggingFace(llm=endpoint)

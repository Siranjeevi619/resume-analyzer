from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

import os

CHROMA_DIR="chroma_db"

embedding_model = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def get_chroma(collection_name : str):
    return Chroma(collection_name = collection_name, 
                  embedding_function = embedding_model,
                  persist_directory = CHROMA_DIR)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vectorstore.chroma_client import get_chroma

def store_job_description(jd_text:str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    chunk = splitter.split_text(jd_text)
    chroma = get_chroma("job_description")
    chroma.add_texts(
        texts=chunk,
        metadatas=[{"source": "jd"} for _ in chunk]
    )
    
    chroma.persist()
    return len(chunk)

def match_resume_with_jd(resume_text : str):
    chroma = get_chroma("job_description")
    result = chroma.similarity_search_with_score(resume_text, k=5)
    return result
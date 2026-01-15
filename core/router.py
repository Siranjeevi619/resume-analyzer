from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
import os

from pydantic import BaseModel
from typing import List

from resume.parser import parse_resume
from resume.extractor import extract_section, extract_skills
from resume.schemas import ResumeSections
from jd.analyzer import store_job_description, match_resume_with_jd
from scoring.ats_scoring import calculate_ats_score
from feedback.generator import generate_resume_feedback
from chat.chat_engine import resume_chat
from dotenv import load_dotenv
load_dotenv()

class JDRequest(BaseModel):
    job_description : str
    
class ATSRequest(BaseModel):
    resume_text : str
    resume_skills : List[str]
    job_description : str
    sections : dict
    
    
class ChatRequest(BaseModel):
    session_id : str
    resume_text:str
    job_description : str
    question  : str

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@router.post("/jd/upload")
def upload_jd(request:JDRequest):
    chunks = store_job_description(request.job_description)
    return {"message":"Job description stored", "chunks":chunks}


@router.post("/jd/match")
def match_resume(request : JDRequest):
    result = match_resume_with_jd(request.job_description)
    return [
        {
        "score":score,
        "matched_text":doc.page_content
        }
        for doc, score in result
    ]


@router.post("/ats/score")
def ats_score(request:ATSRequest):
    return calculate_ats_score(
            resume_text=request.resume_text,
            resume_skills=request.resume_skills,
            jd_text=request.job_description,
            sections=request.sections
        )


@router.post("/resume/upload", response_model=ResumeSections)
async def upload_resume(file: UploadFile = File(...)):
    file_id = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = parse_resume(file_path)
    sections = extract_section(raw_text)
    skills = extract_skills(raw_text)

    return ResumeSections(
        summary=sections.get("summary"),
        skills=skills,
        experience=sections.get("experience"),
        education=sections.get("education"),
        projects=sections.get("projects"),
        raw_text=raw_text
    )


class FeedbackRequest(BaseModel):
    resume_text:str
    resume_skills :  List[str]
    job_description:str
    ats_result:dict
    

@router.post("/feedback")
def resume_feedback(request : FeedbackRequest):
    return generate_resume_feedback(resume_text= request.resume_text, resume_skills=request.resume_skills,   job_description=request.job_description,
        ats_result=request.ats_result)
    
    
@router.post("/resume/chat")
def resume_chat_api(request: ChatRequest):
    answer = resume_chat(
        session_id=request.session_id,
        resume_text=request.resume_text,
        job_description=request.job_description,
        question=request.question
    )
    return {"answer": answer}
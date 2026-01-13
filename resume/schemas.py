from pydantic import BaseModel
from typing import Optional , List

class ResumeSections(BaseModel):
    summary : Optional[str] = None
    skills : List[str] = []
    experience :Optional[str] = None
    education:Optional[str] = None
    raw_text : str
    
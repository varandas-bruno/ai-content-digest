from pydantic import BaseModel, HttpUrl
from typing import Optional


class DigestRequest(BaseModel):
    url: HttpUrl
    language: Optional[str] = "en"

class DigestResponse(BaseModel):
    url: str
    source: str
    summary: str
    relevance_score: float
    key_points: list[str]
    tags: list[str]
    
    
    
    
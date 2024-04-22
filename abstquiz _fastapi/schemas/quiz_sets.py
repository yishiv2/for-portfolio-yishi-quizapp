from typing import List, Optional
from pydantic import BaseModel


class QuizSetResponse(BaseModel):
    id: str
    title: str
    category: Optional[str] = None
    tag: Optional[List[str]] = []


class QuizSetCreateRequest(BaseModel):
    title: str
    category: Optional[str] = None
    tag: Optional[List[str]] = []
    # quizzes: Optional[List[QuizCreateRequest]] = None
    # user_id: Optional[str] = None

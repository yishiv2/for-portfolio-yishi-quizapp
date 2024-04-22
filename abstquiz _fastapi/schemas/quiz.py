from typing import Optional, List

from pydantic import BaseModel

# レスポンスモデル


class QuizResponse(BaseModel):
    id: str  # ドキュメントID
    quiz_set_id: Optional[str]
    image: str
    answer: str
    hints: Optional[List[str]] = []
    explanation: str = None


class QuizDetailResponse(QuizResponse):
    pass

# リクエストスキーマ


class QuizCreateRequest(BaseModel):
    quiz_set_id: str
    image: str
    answer: str
    hint: List[str]
    explanation: str
    user_id: str
    imgae_generate_prompt: Optional[str]


class QuizUpdateRequest(BaseModel):
    quiz_set_id: Optional[str]
    image: Optional[str]
    answer: Optional[str]
    hint: Optional[List[str]]
    explanation: Optional[str]
    user_id: str
    imgae_generate_prompt: Optional[str]

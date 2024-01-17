from typing import Optional
from pydantic import BaseModel, conint


class FeedbackModel(BaseModel):
    rating: conint(ge=0, le=5)
    user_id: int
    page: str
    description: Optional[str]


class FeedbackUpdateModel(BaseModel):
    rating: Optional[conint(ge=0, le=5)]
    user_id: Optional[int]
    page: Optional[str]
    description: Optional[str]


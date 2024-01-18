from typing import Optional
from pydantic import BaseModel, conint


class FeedbackModel(BaseModel):
    rating: conint(ge=0, le=5)
    user_id: int
    referrer: Optional[str]
    description: str
    user_agent: Optional[str]


class FeedbackUpdateModel(BaseModel):
    rating: Optional[conint(ge=0, le=5)]
    user_id: Optional[int]
    referrer: Optional[str]
    description: Optional[str]

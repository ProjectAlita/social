from typing import Optional
from pydantic import AnyUrl, BaseModel

from pylon.core.tools import log


class UserModel(BaseModel):
    user_id: int
    avatar: Optional[AnyUrl]
    title: Optional[str]
    description: Optional[str]


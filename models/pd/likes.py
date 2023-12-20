from typing import Optional
from pydantic import BaseModel

from pylon.core.tools import log
from ...models.enums.entity import EntityType


class LikeModel(BaseModel):
    entity: EntityType
    user_id: int
    project_id: Optional[int]
    entity_id: int


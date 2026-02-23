from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from app.models.reflection_model import QuestReflectionModel

class QuestModel(BaseModel):
    id: str
    name: str
    description: Optional[str]
    expReward: int
    isSuccess: bool

    folderId: str
    reflection: List[QuestReflectionModel]

    createdAt: datetime
    deadLineAt: datetime
    completedAt: Optional[datetime]


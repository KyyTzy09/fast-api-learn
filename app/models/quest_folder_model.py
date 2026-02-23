import datetime
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from app.models.quest_model import QuestModel
from datetime import datetime
from app.models.reflection_model import QuestReflectionModel


class QuestFolderRequestModel(BaseModel):
    folder: str
    isSuccess: bool
    deadline: datetime
    completedAt: Optional[datetime]
    reflections: List[Optional[QuestReflectionModel]]

    #     {
    #     "folder": "Tugas Coding",
    #     "isSuccess": false,
    #     "deadline": "2009-04-11T14:00:00.000Z",
    #     "completedAt": null,
    #     "reflections": [
    #         {
    #             "questLevel": "NORMAL",
    #             "reason": "Malas",
    #             "type": "FAILED"
    #         }
    #     ]
    # },


class QuestFolderModel(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: FolderStatus

    userId: str
    quests: List[QuestModel]

    createdAt: datetime
    endedAt: Optional[datetime]
    updatedAt: datetime


class FolderStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"

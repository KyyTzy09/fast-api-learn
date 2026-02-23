import datetime
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class QuestReflectionModel(BaseModel):
    reason: str
    questLevel: QuestLevel
    type: ReflectionType

class QuestLevel(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class ReflectionType(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

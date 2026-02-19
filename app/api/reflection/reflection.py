from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.ai.llm.client import aiClient as model
from app.ai.llm.loader import load_prompt
import json
from app.deps.deps import verify_token

reflection_router = APIRouter()

class Quest(BaseModel):
    quest_id: str
    issuccess: bool

class QuestHistory(BaseModel):
    folder: str
    quests: List[Quest]

class CreateReflectionRequest(BaseModel):
    reflection: Dict[str, str]
    quest_history: Dict[str, List[QuestHistory]]


@reflection_router.post("/")
async def create_reflection(
    request: CreateReflectionRequest, _: bool = Depends(verify_token)
):
    try:
        prompt_tmplt = load_prompt("user_reflection.prompt")
        prompt = prompt_tmplt.replace(
            "{{payload_json}}",
            json.dumps(request.model_dump(), ensure_ascii=False, indent=2),
        )

        response = await model.generate(prompt)
        return {"message": "Reflection generated", "reflection": response}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

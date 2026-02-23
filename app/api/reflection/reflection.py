from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from app.ai.llm.client import aiClient as model
from app.ai.llm.loader import load_prompt
import json
from app.deps.deps import verify_token
from app.models.quest_folder_model import QuestFolderModel, QuestFolderRequestModel
from app.helpers.reflection_analytic_converter import ReflectionAnalyticConverter

reflection_router = APIRouter()


class CreateReflectionRequest(BaseModel):
    histories: List[QuestFolderRequestModel]


@reflection_router.post("/")
async def create_reflection(
    request: CreateReflectionRequest, _: bool = Depends(verify_token)
):
    converter = ReflectionAnalyticConverter()
    try:
        convertedResult = converter.convert(data=request.histories)
        # prompt_tmplt = load_prompt("user_reflection.prompt")
        # prompt = prompt_tmplt.replace(
        #     "{{payload_json}}",
        #     json.dumps(request.model_dump(), ensure_ascii=False, indent=2),
        # )

        # response = await model.generate(prompt)
        return {"message": "Reflection generated", "data": convertedResult}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

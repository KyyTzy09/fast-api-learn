from fastapi import APIRouter
from app.deps.deps import verify_token
import os
from app.ai.llm.client import aiClient
from app.api.reflection.reflection import reflection_router

api_router = APIRouter()

api_router.include_router(reflection_router, prefix="/reflection", tags=["Reflection"])
@api_router.get("/ping")
def Pong():
    return {"message": "Pong", "success": True}


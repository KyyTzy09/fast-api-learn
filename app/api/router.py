from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.deps.deps import verify_token

api_router = APIRouter()

class CreateMessageRequest(BaseModel) :
    username : str
    message : str

@api_router.post("/message")
async def tes(request: CreateMessageRequest,  _: bool = Depends(verify_token)):
    if not request.message.strip() :
        raise HTTPException(status_code=400, detail="Message tidak boleh kosong")
    return {"message": "", "data": request}


@api_router.get("/ping")
def Pong():
    return {"message": "Pong", "success": True}


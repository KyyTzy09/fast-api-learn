from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import BaseModel
from app.deps.deps import verify_token
import google.generativeai as genai
import os

api_router = APIRouter()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")
class CreateMessageRequest(BaseModel) :
    username : str
    message : str

@api_router.post("/message")
async def tes(request: CreateMessageRequest,  _: bool = Depends(verify_token)):
    if not request.message.strip() :
        raise HTTPException(status_code=400, detail="Message tidak boleh kosong")
    
    try :
        res = await model.generate_content_async(request.message)
        return {"message": "Yes", "data": res.text}
    except Exception as e :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@api_router.get("/ping")
def Pong():
    return {"message": "Pong", "success": True}


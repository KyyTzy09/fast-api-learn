import sys
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from api.router import api_router
from fastapi import FastAPI
from app.api.router import api_router
from app.configs.config import settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
load_dotenv(PROJECT_ROOT / ".env")

app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix="/api/v1")

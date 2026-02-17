from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parents[1] / "prompts"

@lru_cache(maxsize=32)
def load_prompt(filename: str) -> str:
    path = BASE_DIR / filename
    
    if not path.exists():
        raise FileNotFoundError(f"Root Prompt not found {filename}")
    
    return path.read_text(encoding="utf-8")
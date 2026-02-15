from fastapi import Header, HTTPException, status


def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer Required"
        )

    token = authorization.replace("Bearer ", "")
    if token != "AI-API":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    
    return True

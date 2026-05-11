from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.security import decode_token

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str=Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_error = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_error
    
    user_id = payload.get("sub")
    from app.models.user_model import User
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_error
    return user
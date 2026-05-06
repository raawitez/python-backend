from fastapi import Depends
from app.services.user_service import UserService
from sqlalchemy.orm import Session
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_current_user_id() -> int:
    return 1
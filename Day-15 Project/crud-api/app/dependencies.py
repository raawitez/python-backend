from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.user_service import UserService
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


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db:    Session = Depends(get_db)
):
    error = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_token(token)
    if not payload:
        raise error

    user_id = payload.get("sub")
    if not user_id:
        raise error

    from app.models.user_model import User
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise error

    return user
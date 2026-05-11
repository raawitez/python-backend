from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.dependencies import get_db
from app.models.user_model import User
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db:Session = Depends(get_db)):
    existing = db.query(User).filter(User.email==user.email).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Email {user.email} is already registered"
        )
    
    hashed = hash_password(user.password)
    new_user = User(
        name = user.name,
        email = user.email,
        age = user.age,
        password = hashed,
        bio = user.bio
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    token = create_access_token(user_id=user.id, email = user.email)
    return{
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), current_user: User = Depends()):
    return current_user

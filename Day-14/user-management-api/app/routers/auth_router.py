from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.dependencies import get_db, get_current_user
from app.models.user_model import User
from app.auth.security import hash_password, verify_password, create_access_token
from app.tasks.email_tasks import send_welcome_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db:Session = Depends(get_db)
    ):
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

    background_tasks.add_task(
        send_welcome_email,
        email=new_user.email,
        name=new_user.name
    )

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
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return current_user

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=1, le=120)
    password: str = Field(min_length=6)
    bio: Optional[str] = Field(default=None, max_length=200)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    bio: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=1, le=120)
    bio: Optional[str] = Field(default=None, max_length=200)


@router.get("/", response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(
        name=user.name,
        email=user.email,
        age=user.age,
        password=user.password,
        bio=user.bio
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.update_user(
        user_id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
        password=user.password,
        bio=user.bio
    )


@router.patch("/{user_id}", response_model=UserResponse)
def partial_update_user(
    user_id: int,
    user: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return service.partial_update_user(
        user_id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
        bio=user.bio
    )


@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)
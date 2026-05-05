from fastapi import APIRouter, Depends
from typing import List

from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse], summary="List all users")
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{user_id}",response_model=UserResponse, summary="Get a user by ID")
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@router.post("/", response_model=UserResponse, status_code=201, summary="Create a new user")
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(
        name= user.name,
        email = user.email,
        age = user.age,
        password = user.password,
        bio = user.bio
        )

@router.put("/{user_id}", response_model=UserResponse, summary="Fully replace a user (all fields required)")
def update_user(user_id: int,user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.update_user(
        user_id = user_id,
        name = user.name,
        email = user.email,
        age = user.age,
        password = user.password,
        bio = user.bio
    )

@router.patch("/{user_id}", response_model=UserResponse, summary="Partially update a user (send only changed fields)")
def partial_update_user(user_id: int, user: UserUpdate, service: UserService = Depends(get_user_service)):
    return service.partial_update_user(
        user_id = user_id,
        name = user.name,
        email = user.email,
        age = user.age,
        bio = user.bio
    )

@router.delete("/{user_id}", status_code=204, summary="Delete a user")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.delete_user(user_id)

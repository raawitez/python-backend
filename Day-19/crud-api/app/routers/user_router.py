from fastapi import APIRouter, Depends, Response, BackgroundTasks
from typing import List

from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.dependencies import get_user_service, get_current_user
from app.models.user_model import User
from app.tasks.email_tasks import send_account_deletion_email

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse], summary="List all users")
def list_users(response: Response, service: UserService = Depends(get_user_service)):
    result = service.get_all_users()
    if isinstance(result, list) and len(result)>0:
        response.headers["X-Cache"] = "HIT" if service.last_cache_hit else "MISS"
    return result

@router.get("/{user_id}",response_model=UserResponse, summary="Get a user by ID")
def get_user(user_id: int, response: Response,service: UserService = Depends(get_user_service)):
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

@router.patch("/{user_id}", response_model=UserResponse)
def partial_update_user(
    user_id: int,
    user: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)   
):
    return service.partial_update_user(
        user_id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
        bio=user.bio
    )

@router.delete("/{user_id}", summary="Delete a user — requires login")
def delete_user(
    user_id: int,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    user = service.get_user_by_id(user_id)
    result = service.delete_user(user_id)
    background_tasks.add_task(
        send_account_deletion_email,
        email=user["email"],
        name=user["name"]
    )
    return result
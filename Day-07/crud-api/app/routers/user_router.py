from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.data import store

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name:str = Field(
        min_length=2,
        max_length=50,
        description="Full name of the user"
    )
    email: EmailStr = Field(
        description = "Must be a valid email address"
    )
    age:int = Field(
        ge=1,
        le=120,
        description = "Age must be between 1 and 120"
    )
    password: str = Field(
        min_length = 6,
        description = "Minimum 6 characters"
    )
    bio: Optional[str] = Field(
        default = None,
        max_length = 200,
        description = "Short bio, optional"
    )

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    bio: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = Field(
        default = None,
    )
    email: Optional[str] = None
    age: Optional[str] = None

@router.get("/")
def list_users():
    return list(store.users.values())

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in store.users:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    return store.users[user_id]

@router.post("/", response_model=UserResponse,status_code=201)
def create_user(user: UserCreate):
    global_next_id = store.next_id
    for existing_user in store.users.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=409,
                detail=f"Email {user.email} already registered"
            )
        
    new_user = {
        "id" : global_next_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
        "password": user.password,
        "bio": user.bio
    }
    store.users[global_next_id] = new_user
    store.next_id += 1
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    if user_id not in store.users:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    updated_user={
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
        "password": user.password,
        "bio": user.bio
    }

    store.users[user_id] = updated_user
    return updated_user

@router.patch("/{user_id}")
def partial_update_user(user_id: int, user: UserUpdate):
    if user_id not in store.users:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    existing = store.users[user_id]
    if user.name is not None:
        existing["name"] = user.name
    
    if user.email is not None:
        existing["email"] = user.email
    
    if user.age is not None:
        existing["age"] = user.age
    
    store.users[user_id] = existing
    return existing

@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in store.users:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    del store.users[user_id]
    return {"message": f"User {user_id} deleted successfully"}
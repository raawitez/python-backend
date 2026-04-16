from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.data import store

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name:str
    email:str
    age:int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[str] = None

@router.get("/")
def list_users():
    return list(store.users.values())

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id not in store.users:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )
    return store.users[user_id]

@router.post("/",status_code=201)
def create_user(user: UserCreate):
    global_next_id = store.next_id

    new_user = {
        "id" : global_next_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }
    store.users[global_next_id] = new_user
    store.next_id += 1
    return new_user

@router.put("/{user_id}")
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
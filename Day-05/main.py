from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User API", version="1.0")

users = []
next_id = 1

class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/users")
def list_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=404,
        detail=f"User {user_id} not found"
    )


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    global next_id

    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email
    }

    users.append(new_user)
    next_id += 1

    return new_user
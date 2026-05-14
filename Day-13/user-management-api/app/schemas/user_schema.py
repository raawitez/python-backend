from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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

    class Config:
        from_attributes = True
        
class UserUpdate(BaseModel):
    name:  Optional[str]      = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age:   Optional[int]      = Field(default=None, ge=1, le=120)
    bio:   Optional[str]      = Field(default=None, max_length=200)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
    email: str
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
        description="Full name",
        examples=["Teja"]
    )
    email: EmailStr = Field(
        description="Valid email address"
        examples=["teja@gmail.com"]

    )
    age: int = Field(
        ge=1,
        le=120,
        description="Age between 1 and 120",
        examples=[22]
    )
    password: str = Field(
        min_length=6,
        description="Minimum 6 characters",
        examples=["teja123"]
    )
    bio: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Short bio, optional",
        examples=["Building API"]
    )

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_digits=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=1, le=120)
    bio: Optional[str] = Field(default=None, max_length=200)
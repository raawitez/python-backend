from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code = 404,
                detail=f"User {user_id} not found"
            )
        return user
    
    def create_user(self, name:str, email: str, age:int, password: str, bio=None):
        existing = self.db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Email {email} already registered"
            )
        
        new_user = User(
            "id": user_id,
            "name": name,
            "email": email,
            "age": age,
            "password": password,
            "bio": bio
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update_user(self, user_id: int, name: str, email: str, age: int, password: str, bio=None):
        user = self.get_user_by_id(user_id)  
        user.name = name
        user.email = email
        user.age = age
        user.password = password
        user.bio = bio

        self.db.commit()
        self.db.refresh(user)
        return user

    def partial_update_user(self, user_id: int, name=None, email=None, age=None, bio=None):
        user = self.get_user_by_id(user_id)  
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if age is not None:
            user.age = age
        if bio is not None:
            user.bio = bio

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)   
        self.db.delete(user)
        self.db.commit()
        return {"message": f"User {user_id} deleted successfully"}
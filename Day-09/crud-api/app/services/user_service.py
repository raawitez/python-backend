from fastapi import HTTPException
from app.data import store

class UserService:
    def get_all_users(self):
        return list(store.users.values())
    
    def get_user_by_id(self, user_id: int):
        if user_id not in store.users:
            raise HTTPException{
                status_code = 404,
                detail=f"User {user_id} not found"
            }
        return store.users[user_id]
    
    def create_user(self, name:str, email: str, age:int, password: str, bio=None):
        for existing in store.users.values():
            if existing["email"]==email:
                raise HTTPException(
                    status_code=409,
                    detail=f"Email {email} already registered"
                )
        user_id = store.next_id
        new_user = {
            "id": user_id,
            "name": name,
            "email": email,
            "age": age,
            "password": password,
            "bio": bio
        }

        store.users[user_id] = new_user
        store.next_id += 1
        return new_user
    
    def update_user(self, user_id: int, name: str, email: str, age: int, password: str, bio=None):
        self.get_user_by_id(user_id)  

        updated_user = {
            "id": user_id,
            "name": name,
            "email": email,
            "age": age,
            "password": password,
            "bio": bio
        }

        store.users[user_id] = updated_user
        return updated_user

    def partial_update_user(self, user_id: int, name=None, email=None, age=None, bio=None):
        existing = self.get_user_by_id(user_id)  
        if name is not None:
            existing["name"] = name
        if email is not None:
            existing["email"] = email
        if age is not None:
            existing["age"] = age
        if bio is not None:
            existing["bio"] = bio

        store.users[user_id] = existing
        return existing

    def delete_user(self, user_id: int):
        self.get_user_by_id(user_id)   
        del store.users[user_id]
        return {"message": f"User {user_id} deleted successfully"}
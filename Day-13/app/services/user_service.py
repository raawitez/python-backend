from fastapi import HTTPException
from sqlalchemy.orm import Session
from loguru import logger
from app.models.user_model import User
from app.cache.redis_client import(
    get_cache, set_cache, delete_cache, delete_pattern,
    CACHE_ALL_USERS, CACHE_USER,
    TTL_MEDIUM, TTL_LONG
)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        cached = get_cache(CACHE_ALL_USERS)
        if cached is not None:
            logger.info("Cache HIT - all_users")
            return cached
        
        logger.info("Cache MISS - querying database for all_users")
        users = self.db.query(User).all()
        users_data = []
        for u in users:
            user_dict = {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "age": u.age,
                "bio": u.bio
            }
            users_data.append(user_dict)

        set_cache(CACHE_ALL_USERS, users_data, TTL_MEDIUM)
        return users_data

    def get_user_by_id(self, user_id: int):
        cache_key = f"user:{user_id}"

        cached = get_cache(cache_key)
        if cached is not None:
            logger.info(f"Cache HIT - {cache_key}")
            return cached
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User {user_id} not found"
            )

        user_data ={
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "bio": user.bio
        }
        set_cache(cache_key, user_data, TTL_LONG)
        return user_data

    def create_user(self, name:str, email:str, age:int, password: str, bio=None):
        existing = self.db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Email {email} already registered"
            )
        
        new_user = User(
            name = name,
            email = email,
            age = age,
            password = password,
            bio = bio
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        delete_cache(CACHE_ALL_USERS)
        logger.info(f"Cache invalidated after creating a new user {new_user.id}")

        return new_user
    
    def update_user(self, user_id:int, name:str, email:str, age: int, password:str,bio = None):
        user = self.get_user_by_id(user_id)
        existing = self.db.query(User).filter(User.email == email).first()
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=409,
                detail=f"Email {email} already registered"
            )
        user.name = name
        user.email = email
        user.password = password
        user.age = age
        user.bio = bio
        self.db.commit()
        self.db.refresh(user)

        delete_cache(CACHE_ALL_USERS)
        delete_cache(f"user:{user_id}")
        logger.info(f"Cache invalidated after updating user {user_id}")
        return user
    
    def partial_update_user(self, user_id:int, name = None, email = None, age= None, bio =None):
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

        delete_cache(CACHE_ALL_USERS)
        delete_cache(f"user:{user_id}")
        return user
    
    def delete_user(self, user_id:int):
        user = self.get_user_by_id(user_id)
        self.db.delete(user)
        self.db.commit()

        delete_cache(CACHE_ALL_USERS)
        delete_cache(f"user:{user_id}")
        logger.info(f"Cache invalidated after deleting user {user_id}")
        return {"message": f"User {user_id} deleted successfully"}
    
    def _get_user_or_404(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User {user_id} not found"
            )
        return user
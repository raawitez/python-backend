from fastapi import FastAPI
from app.routers import user_router

app = FastAPI(
    title="User CRUD API",
    version="1.0",
    description="Full CRUD API for User Management"
)

app.include_router(user_router.router)
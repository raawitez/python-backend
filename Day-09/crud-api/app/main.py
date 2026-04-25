from fastapi import FastAPI
from app.routers import user_router
from app.models import user_model
from app.database import Base, engine

app = FastAPI(
    title="User CRUD API",
    version="1.0",
    description="Full CRUD API with SQLite database"
)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
    
app.include_router(user_router.router)
from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.models import user_model
from app.routers import user_router, auth_router
from app.middleware.logging_middleware import log_requests
from app.core.logger import setup_logger
from app.core.exceptions import global_exception_handler
from app.auth.security import hash_password
from app.cache.redis_client import check_redis_connection

setup_logger()

from loguru import logger

app = FastAPI(
    title="User Management API",
    version="3.0",
    description="User Management API with Auth, Logging and Middleware"
)

app.middleware("http")(log_requests)

app.add_exception_handler(Exception, global_exception_handler)

@app.on_event("startup")
def startup():
    logger.info("Starting User Management API...")

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified")
    
    check_redis_connection()
    logger.info("API startup complete")
    
    db = SessionLocal()
    try:
        from app.models.user_model import User
        if db.query(User).count()==0:
            test_users = [
                User(name = "Teja", email="teja@gmail.com",
                age = 22, password = hash_password("Teja@123"), bio = "Backend Dev"),
                User(name = "Ravi", email="ravi@gmail.com",
                age = 22, password = hash_password("Ravi@123"), bio = "Frontend Dev")
            ]
            db.add_all(test_users)
            db.commit()
            logger.info("Database seeded with test users")
        else:
            count = db.query(User).count()
            logger.info(f"Database has {count} existing users")

    finally:
        db.close()

    logger.info("API startup complete. Listening for requests...")

    app.include_router(auth_router.router)
    app.include_router(user_router.router)

    @app.get("/", tags=["Health"])
    def root():
        return{
            "message": "User Management API running",
        "version": "3.0",
        "docs": "/docs"
        }
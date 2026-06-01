from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager

from app.core.logger import setup_logger
from app.core.exceptions import global_exception_handler

setup_logger()

from app.database import Base, engine, SessionLocal
from app.models import user_model
from app.routers import user_router, auth_router
from app.middleware.logging_middleware import log_requests
from app.cache.redis_client import check_redis_connection
from app.messaging.rabbitmq_client import publisher

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("="*50)
    logger.info("User Management API - Starting Up")
    logger.info("="*50)

    # Database
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready")

    # Redis
    redis_ok = check_redis_connection()
    if not redis_ok:
        logger.warning("Redis unavailable - caching disabled")

    #RabbitMQ
    publisher.connect()
    if publisher.channel:
        logger.info("RabbitMQ publisher connected")
    else:
        logger.warning("RabbitMQ unavailable - events will be skipped")

    # Seeding Database 
    db = SessionLocal()
    try:
        from app.models.user_model import User
        from app.auth.security import hash_password

        if db.query(User).count()==0:
            test_users = [
                User(
                    name="Teja",
                    email="teja@gmail.com",
                    age = 22,
                    password=hash_password("Teja@123"),
                    bio = "Backend Developer"
                ),
                User(
                    name="Ravi ",
                    email="ravi@gmail.com",
                    age=24,
                    password=hash_password("Ravi@123"),
                    bio="Full stack developer"
                ),
            ]
            db.add_all(test_users)
            db.commit()
            logger.info("Database seeded")
        else:
            logger.info(f"Database has {db.query(User).count()} users")
    finally:
        db.close()

    logger.info("="*50)
    logger.info("API ready -> http://localhost:8000/docs")
    logger.info("="*50)

    yield
    logger.info("API shutting down...")
    publisher.disconnect()
    logger.info("Goodbye...")

# app
app = FastAPI(
    title="User Management API",
    version="4.0",
    description="FastAPI + RabbitMQ event-driven integration",
    lifespan=lifespan
)

# Middleware
app.middleware("http")(log_requests)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)

# Routers
app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/", tags["Health"])
def root():
    return{
        "name": "User Management API",
        "version": "4.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
def health():
    from app.cache.redis_client import redis_client

    db_status = "ok"
    redis_status = "ok"
    mq_status = "ok"

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
    except Exception:
        db_status = "error"

    try:
        redis_client.ping()
    except Exception:
        redis_status = "error"

    if not publisher.channel:
        mq_status = "error"
    
    overall = (
        "healthy"
        if all(s=="ok" for s in [db_status, redis_status, mq_status])
        else "degraded"
    )

    return{
        "status": overall,
        "database": db_status,
        "redis": redis_status,
        "rabbitmq": mq_status
    }
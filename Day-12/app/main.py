from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.models import user_model
from app.routers import user_router, auth_router
from app.auth.security import hash_password

app = FastAPI(
    title="User Management API",
    version="2.0",
    description="""
A complete User Management API built with FastAPI + SQLAlchemy.

Features:
- Full CRUD operations
- SQLite persistent storage
- Pydantic validation
- Layered architecture (Router -> Service -> DataBase)
"""
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        from app.models.user_model import User
        if db.query(User).count() == 0:
            test_users = [
                User(
                    name="Teja",
                    email = "teja@gmail.com",
                    age = 22,
                    password = hash_password("Teja@123"),
                    bio = "Backend Developer"
                ),
                User(
                    name="Ravi",
                    email="ravi@gmail.com",
                    age = 22,
                    password = hash_password("Ravi@123"),
                    bio = "Full stack developer"
                ),
            ]
            db.add_all(test_users)
            db.commit()
            print("Database seeded with 2 test users")
        else:
            count = db.query(User).count()
            print(f"Database already has {count} users - skipping seed")

    finally:
        db.close()

app.include_router(user_router.router)
app.include_router(auth_router.router)


@app.get("/", tags=["Health"])
def root():
    return{
        "message":"User Management API is running",
        "version":"2.0",
        "docs":"/docs"
    }
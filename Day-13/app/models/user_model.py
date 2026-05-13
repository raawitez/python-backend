from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(100),nullable=False)
    bio = Column(String(200), nullable=True)

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email}>"
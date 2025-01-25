from sqlalchemy import Column , Integer , String
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    name = Column(String(50))
    email = Column(String(100) , unique=True)
    password = Column(String(120))
    is_student = Column(Integer)
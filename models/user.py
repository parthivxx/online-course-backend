from sqlalchemy import Column , Integer , String , Text
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    name = Column(String(50))
    email = Column(String(100) , unique=True)
    password = Column(Text)
    is_student = Column(Integer)
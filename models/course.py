from .database import Base
from sqlalchemy import Integer , String , Column , Float

class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer , primary_key=True)
    title = Column(String , unique=True)
    description = Column(String)
    duration = Column(Integer)
    ratings = Column(Float)
    


from sqlalchemy import Column , Integer , String , Text , ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    name = Column(String(50))
    email = Column(String(100) , unique=True)
    password = Column(Text)
    is_student = Column(Integer)
    courses = relationship('Course' , back_populates="intstructor")


class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer , primary_key=True)
    course_title = Column(String(150))
    course_description = Column(Text)
    course_duration = Column(Integer)
    instructor_id = Column(Integer , ForeignKey='users.id')
    instructor = relationship('User' , back_populates="courses")

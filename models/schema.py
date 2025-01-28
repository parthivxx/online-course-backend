from sqlalchemy import Column , Integer , String , Text , ForeignKey , PrimaryKeyConstraint
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True)
    name = Column(String(50))
    email = Column(String(100) , unique=True)
    password = Column(Text)
    is_student = Column(Integer)
    courses = relationship('Course' , back_populates="instructor")
    enrolled_courses = relationship('Enrolled' , back_populates="user")


class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer , primary_key=True)
    course_title = Column(String(150))
    course_description = Column(Text)
    course_duration = Column(Integer)
    instructor_id = Column(Integer , ForeignKey('users.id'))
    instructor = relationship('User' , back_populates="courses")
    courses_enrolled = relationship('Enrolled' , back_populates='course')


class Enrolled(Base):
    __tablename__ = 'enrolled'
    user_id = Column(Integer ,ForeignKey('users.id') ,  primary_key=True)
    course_id = Column(Integer , ForeignKey('courses.course_id') , primary_key = True)
    

    __tableargs__ = PrimaryKeyConstraint('user_id' , 'course_id')

    user = relationship('User' , back_populates='enrolled_courses')
    course = relationship('Course' , back_populates='courses_enrolled')
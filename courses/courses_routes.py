from flask import Blueprint , request , jsonify , g
from models.schema import Course , User , Enrolled
from models.database import get_db
import jwt 
import os
from middleware.auth_decorator import auth_required
from sqlalchemy import and_

courses_bp = Blueprint('courses' , __name__)

@courses_bp.route("/courses" , methods=["POST"])
@auth_required
def create_course():
    data = request.get_json()
    instructor_id = request.user
    try:
        title  , description , duration = data["title"] , data["description"] , int(data["duration"])
        db = get_db()
        new_course = Course(instructor_id = instructor_id , course_title = title , course_description = description , course_duration = duration)
        db.add(new_course)
        db.commit()
        response = dict()
        return jsonify({"courseId" : new_course.course_id , "success" : True}) , 200
    except Exception as e:
        db.rollback()
        return jsonify({"error" : str(e)}) , 400
    
@courses_bp.route("/course" , methods=["GET"])
@auth_required
def get_course():
    user_id = g.user
    course_id = request.args.get("courseId")

    if not course_id:
        return jsonify({"error": "courseId parameter is required"}), 400
    try:
        db = get_db() 
        course = db.query(Course).filter(Course.course_id == course_id).first()
        instructor_name = db.query(User).filter(User.id == course.instructor_id).first().name

        is_enrolled = True if db.query(Enrolled).filter(and_(Enrolled.user_id ==user_id , Enrolled.course_id == course.course_id )).count() > 0 else False
        if not course:
            return jsonify({"error": "Course not found"}), 404

        return jsonify({
            "courseId": course.course_id,
            "title": course.course_title,
            "description": course.course_description,
            "duration": course.course_duration,
            "instructorName": instructor_name,
            "rating" : -1,
            "isEnrolled" : is_enrolled,
            "instructorId" : course.instructor_id,
            "files" : []
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@courses_bp.route("/courses" , methods=["GET"])
@auth_required
def get_all_courses():
    user_id = g.user
    try:
        db = get_db()
        all_courses_rows = db.query(Course).all()
        courses_data = []
        for course in all_courses_rows:
            course_dict = {
                "courseId": course.course_id,
                "title": course.course_title,
                "duration" : course.course_duration,
                "instructorName" : db.query(User).filter(User.id == course.instructor_id).first().name,
                "instructorId" : course.instructor_id,
                "rating" : -1,
                "isEnrolled" : True if db.query(Enrolled).filter(and_(Enrolled.user_id ==user_id , Enrolled.course_id == course.course_id )).count() > 0 is not None else False
            }
            courses_data.append(course_dict)
        return jsonify({"courses" : courses_data}) , 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 500
    
@courses_bp.route("/enroll" , methods=["POST"])
@auth_required
def enroll():
    course_id = request.get_json()["courseId"]
    user_id = g.user
    try:
        db = get_db()
        new_enrollment = Enrolled(user_id = user_id , course_id = course_id)
        db.add(new_enrollment)
        db.commit()
        course = db.query(Course).filter(Course.course_id == course_id).first()
        return jsonify({
            "courseId": course.course_id,
            "title": course.course_title,
            "description": course.course_description,
            "duration": course.course_duration,
            "instructorName": db.query(User).filter(User.id == user_id).first().name,
            "rating" : -1,
            "isEnrolled" : True,
            "files" : []
        }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error" : str(e)}) , 500
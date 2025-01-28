from flask import Blueprint , request , jsonify
from models.schema import Course , User
from models.database import get_db
import jwt 
import os
from middleware.auth_decorator import auth_required

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
    try:
        course_id = request.args.get("courseId")

        if not course_id:
            return jsonify({"error": "courseId parameter is required"}), 400

        db = get_db() 
        course = db.query(Course).filter_by(course_id=course_id).first()
        instructor_name = db.query(User).filter(User.id == course.course_id).first().name
        if not course:
            return jsonify({"error": "Course not found"}), 404

        return jsonify({
            "courseId": course.course_id,
            "title": course.course_title,
            "description": course.course_description,
            "duration": course.course_duration,
            "instructorName": instructor_name,
            "rating" : -1
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
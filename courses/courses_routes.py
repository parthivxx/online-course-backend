from flask import Blueprint , request , jsonify
from models.schema import Course
from models.database import get_db

courses_bp = Blueprint('courses' , __name__)

@courses_bp.route("/create-course" , methods=["POST"])
def create_course():
    data = request.get_json()
    try:
        instructor_id  , title  , description , duration = int(data["id"]) , data["title"] , data["description"] , int(data["duration"])
        db = get_db()
        new_course = Course(instructor_id = instructor_id , course_title = title , course_description = description , course_duration = duration)
        db.add(new_course)
        db.commit()
        return jsonify({"courseId" : new_course.course_id , "success" : True}) , 200
    except Exception as e:
        db.rollback()
        return jsonify({"error" : str(e)}) , 400
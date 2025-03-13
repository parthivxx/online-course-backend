from flask import Blueprint , jsonify , request
from models.database import get_db
from models.schema import Question , Quiz
from sqlalchemy import text

quiz_bp = Blueprint('quiz' , __name__)

@quiz_bp.route("/test" , methods=["GET"])
def test():
    return "working just fine"

@quiz_bp.route("/create" , methods=["POST"])
def create_quiz():
    data = request.get_json()

    if not data or 'quizTitle' not in data or 'courseId' not in data or 'questions' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        db = get_db()
        new_quiz = Quiz(course_id=data['courseId'], quiz_title=data['quizTitle'] , quiz_description=data["quizDescription"])
        db.add(new_quiz)
        db.commit()

        i = 1
        for question_data in data['questions']:
            new_question = Question(
                quiz_id=data['courseId'], 
                question_id = i,
                question_text=question_data['questionText'],
                option_1_body=question_data['options'][0],
                option_2_body=question_data['options'][1],
                option_3_body=question_data['options'][2],
                option_4_body=question_data['options'][3],
                correct_option = question_data['correctOption']
            )
            i += 1
            db.add(new_question)
            db.commit()
        
        return jsonify({"message": "new quiz and questions created"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    
@quiz_bp.route("/<int:course_id>" , methods=["GET"])
def get_all(course_id):
    try:
        db = get_db()

        quiz_result = db.execute(
            text("SELECT * FROM quizzes WHERE course_id = :course_id LIMIT 1"),
            {"course_id": course_id}
        ).fetchone()

        if not quiz_result:
            return jsonify({"error": "No quiz found for this course"}), 404


        question_results = db.execute(
            text("SELECT * FROM questions WHERE quiz_id = :quiz_id"),
            {"quiz_id": quiz_result.course_id}
        ).fetchall()

        quiz_data = {
            "courseId": quiz_result.course_id,
            "quizTitle": quiz_result.quiz_title,
            "quizDescription": quiz_result.quiz_description,
            "questions": [
                {
                    "questionId": question.question_id,
                    "questionText": question.question_text,
                    "options": [
                        question.option_1_body,
                        question.option_2_body,
                        question.option_3_body,
                        question.option_4_body,
                    ]
                }
                for question in question_results
            ]
        }

        return jsonify(quiz_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quiz_bp.route("/submit/<int:course_id>" , methods=["POST"])
def submit(course_id):
    try:
        db = get_db()
        selected_options = request.get_json()["selectedOptions"]
        questions = db.execute(
            text("SELECT * FROM questions WHERE quiz_id = :quiz_id"),
            {"quiz_id" : course_id}
        ).fetchall()
        score = 0
        correct_options = []
        for i,question in enumerate(questions):
            if question.correct_option == selected_options[i]:
                score += 1
            correct_options.append(question.correct_option)
        response = {
            "score" : score,
            "correctOptions": correct_options
        }
        return jsonify(response) , 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quiz_bp.route("/delete-all", methods=["DELETE"])
def delete_all_quizzes():
    try:
        db = get_db()
        db.query(Question).delete()
        db.query(Quiz).delete()
        db.commit()
        return jsonify({"message": "All quizzes and associated questions deleted"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
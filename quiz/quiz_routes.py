from flask import Blueprint , jsonify , request
from models.database import get_db
from models.schema import Question , Quiz
from sqlalchemy.orm import joinedload

quiz_bp = Blueprint('quiz' , __name__)

@quiz_bp.route("/test" , methods=["GET"])
def test():
    return "working just fine"

@quiz_bp.route("/create" , methods=["POST"])
def create_quiz():
    data = request.get_json()

    if not data or 'quizTitle' not in data or 'courseId' not in data or 'numberOfQuestions' not in data or 'questions' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        db = get_db()
        new_quiz = Quiz(course_id=data['courseId'], quiz_title=data['quizTitle'], number_of_questions=data['numberOfQuestions'])
        db.add(new_quiz)
        db.commit()

        for question_data in data['questions']:
            new_question = Question(
                quiz_id=question_data['courseId'],  
                question_text=question_data['questionBody'],
                option_1_body=question_data['option1']['body'],
                option_1_correctness=question_data['option1']['correctness'],
                option_2_body=question_data['option2']['body'],
                option_2_correctness=question_data['option2']['correctness'],
                option_3_body=question_data['option3']['body'],
                option_3_correctness=question_data['option3']['correctness'],
                option_4_body=question_data['option4']['body'],
                option_4_correctness=question_data['option4']['correctness']
            )
            db.add(new_question)

        db.commit()
        return jsonify({"message": "new quiz and questions created"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    
@quiz_bp.route("/get-all" , methods=["GET"])
def get_all():
    try:
        db = get_db()
        quizzes = db.query(Quiz).options(joinedload(Quiz.questions)).all()
        quiz_list = [
            {
                # "id": quiz.quiz_id,
                "courseId": quiz.course_id,
                "quizTitle": quiz.quiz_title,
                "numberOfQuestions": quiz.number_of_questions,
                "questions": [
                    {
                        "questionText": question.question_text,
                        "options": [
                            {"body": question.option_1_body, "correctness": question.option_1_correctness},
                            {"body": question.option_2_body, "correctness": question.option_2_correctness},
                            {"body": question.option_3_body, "correctness": question.option_3_correctness},
                            {"body": question.option_4_body, "correctness": question.option_4_correctness}
                        ]
                    }
                    for question in quiz.questions
                ]
            }
            for quiz in quizzes
        ]
        return jsonify(quiz_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quiz_bp.routes("/all-questions")
def get_all_questions():
    

@quiz_bp.routes("/delete-all", methods=["DELETE"])
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
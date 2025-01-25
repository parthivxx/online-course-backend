from flask import Blueprint , jsonify , request
from models import get_db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

@auth_bp.route('/register' , methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields (name, email)"}), 400

    db = get_db()

    try:
        new_user = User(name=data['name'], email = data['email'] , password = data['password'] , is_student = 1)
        db.add(new_user)
        db.commit()
        return jsonify({"message": "User created successfully", "user_id": new_user.id}),201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400

from flask import Blueprint , jsonify , request
from models import get_db
from models.user import User
from werkzeug.security import check_password_hash , generate_password_hash
import copy 
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

@auth_bp.route('/register' , methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data or 'password' not in data or 'role' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()

    existing_user = db.query(User).filter(User.email == data['email']).first()

    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 409
    
    try:
        new_user = User(name=data['name'], email = data['email'] , password = generate_password_hash(data['password']) , is_student = 1 if data['role']=="student" else 0)
        db.add(new_user)
        db.commit()
        response = copy.deepcopy(data)
        response["id"] = new_user.id
        response.pop('password')
        token_content = {'id' : new_user.id}
        token = jwt.encode(token_content , os.getenv('JWT_SECRET') , os.getenv('JWT_ALGO'))
        response['token'] = token
        response['success'] = True

        return jsonify(response),201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400


@auth_bp.route("/login" , methods=["POST"])
def login():
    pass
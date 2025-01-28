from functools import wraps
from flask import request, jsonify , g
import jwt
import os

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Authorization token is missing"}), 401
        
        try:

            decoded_token = int(jwt.decode(token, os.getenv('JWT_SECRET'), os.getenv('JWT_ALGO')).get("id"))
            g.user = decoded_token
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    
    return decorated_function

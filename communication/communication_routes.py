from flask import Blueprint , jsonify ,request
from models.database import get_db
from models.schema import Chat

communication_bp = Blueprint('communication' , __name__)

@communication_bp.route('/',methods=["GET"])
def get_chats():
    username = request.args.get('username')
    try:
        db = get_db()
        chats = db.query(Chat).filter(Chat.student == username).all()

        if not chats:
            return jsonify({"success": False, "message": "No chats found for the given student"}), 404

        response = [
            {"chat_id": chat.chat_id, "teacher": chat.teacher, "student": chat.student}
            for chat in chats
        ]

        return jsonify({"success": True, "chats": response}), 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 500
from flask import Blueprint , jsonify ,request , g
from models.database import get_db
from models.schema import Chat , User , ChatMessage
from middleware.auth_decorator import auth_required

communication_bp = Blueprint('communication' , __name__)

@communication_bp.route('/',methods=["GET"])
def get_chats():
    username = request.args.get('username')
    try:
        db = get_db()
        chats = db.query(Chat).filter(Chat.student == username).all()

        response = [
            {"chatId": chat.chat_id, "receiverId": chat.teacher, "senderId": chat.student
             , "receiverName" : db.query(User).filter(User.id == chat.teacher).first().name}
            for chat in chats
        ]

        chats = db.query(Chat).filter(Chat.teacher == username).all()

        response2 = [
            {"chatId": chat.chat_id, "receiverId": chat.student, "senderId": chat.teacher
             , "receiverName" : db.query(User).filter(User.id == Chat.student).first().name}
            for chat in chats
        ]

        response = response + response2
        return jsonify({"success": True, "chats": response}), 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 500


@communication_bp.route('/<int:chat_id>' , methods=["GET"])
@auth_required
def get_message(chat_id):
    try:
        db = get_db()

        chat_messages = db.query(ChatMessage).filter(chat_id == ChatMessage.chat_id).all()
        response = [
            {"body" : msg.chat_text , "senderId" : msg.sender_id}
            for msg in chat_messages
        ]
        
        return jsonify(response) , 200
    except Exception as e:
        return jsonify({'error' : str(e)}) , 500


@communication_bp.route('/chat' , methods=["POST"])
@auth_required
def create_chat():
    data = request.get_json()
    user_id = g.user
    instructor_id = data.get('instructorId', '')
    try:
        db = get_db()
        chat = Chat.query.filter(
            ((Chat.teacher == user_id) & (Chat.student == instructor_id)) |
            ((Chat.teacher == instructor_id) & (Chat.student == user_id))
        ).first()

        if not chat:
            new_chat = Chat(teacher=instructor_id, student=user_id)
            db.add(new_chat)
            db.commit()
            return jsonify({'msg' : 'new row added'}) , 200
        return jsonify({'msg' : 'no row was added'}) , 200
    except Exception as e:
        return jsonify({"error" : str(e)}) , 500
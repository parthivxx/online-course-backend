from flask import Flask , jsonify
from auth.auth_routes import auth_bp
from courses.courses_routes import courses_bp
from models import teardown_db , Base
from models.database import engine
from cloudinary.upload_bp import upload_bp
from quiz.quiz_routes import quiz_bp
from flask_socketio import SocketIO , join_room , emit , rooms
from flask_cors import CORS
from models.schema import Chat , ChatMessage
from models.database import get_db
from communication.communication_routes import communication_bp

app = Flask(__name__) 
CORS(app , resources={r"/api/*": {"origins": "*"}})

socketio = SocketIO(app , cors_allowed_origins="*")

@app.route("/" , methods=['GET'])
def hello():
     return "Welcome to Online course backend server!!"

app.register_blueprint(auth_bp , url_prefix="/api/auth")
app.register_blueprint(upload_bp , url_prefix="/api")
app.register_blueprint(courses_bp , url_prefix="/api")
app.register_blueprint(quiz_bp , url_prefix="/api/quiz")
app.register_blueprint(communication_bp , url_prefix="/api/communication")
app.teardown_appcontext(teardown_db)

@socketio.on("join")
def on_join(data):
    username = data['username']
    recipient = data['recipient']
    room = f"{min(username, recipient)}_{max(username, recipient)}"
    join_room(room)
    connected_sockets = rooms()  
    print(f"User {username} joined {room}. Connected sockets: {connected_sockets}")
    emit('message', {'msg': f'{username} has entered the chat.'}, room=room)

    try:
        db = get_db()
        chat = Chat.query.filter(
            ((Chat.teacher == username) & (Chat.student == recipient)) |
            ((Chat.teacher == recipient) & (Chat.student == username))
        ).first()

        if not chat:
            new_chat = Chat(teacher=username, student=recipient)
            db.add(new_chat)
            db.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@socketio.on('send_message')
def handle_send_message(data):
    sender = data['sender']
    recipient = data['recipient']
    message = data['message']
    try:
     db = get_db()
     chat = Chat.query.filter(
          ((Chat.teacher == sender) & (Chat.student == recipient)) |
            ((Chat.teacher == recipient) & (Chat.student == sender))
     ).first()
     if not chat:
          emit({'error' : {'msg': 'This chat room does not exist'}}, room=room)
     else:
          new_chat = ChatMessage()
    except Exception as e:
     return jsonify({"error": str(e)}), 500
    
    room = f"{sender}_{recipient}" if sender < recipient else f"{recipient}_{sender}"
    emit('message', {'msg': message , 'sender' : sender , 'receiver' : recipient}, room=room)


with app.app_context():
     Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    socketio.run(app , debug=True)
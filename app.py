from flask import Flask
from auth.auth_routes import auth_bp
from models import teardown_db , Base
from models.database import engine
from cloudinary.upload_bp import upload_bp
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)
app.register_blueprint(auth_bp , url_prefix="/api/auth")
app.register_blueprint(upload_bp , url_prefix="/api")
app.teardown_appcontext(teardown_db)

with app.app_context():
     Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)
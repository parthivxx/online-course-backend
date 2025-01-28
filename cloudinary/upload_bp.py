from flask import jsonify , request , Blueprint , g
import os
from middleware.auth_decorator import auth_required

upload_bp = Blueprint('upload_bp' , __name__)

@upload_bp.route("/upload", methods=["POST"])
@auth_required
def upload():
    course_id = request.get_json()["data"]
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    COURSE_SUBFOLDER = os.path.join(UPLOAD_FOLDER , str(course_id))
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.exists(COURSE_SUBFOLDER):
        os.mkdir(COURSE_SUBFOLDER)
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(COURSE_SUBFOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message" : f"File uploaded successfully at {file_path}"}) , 200
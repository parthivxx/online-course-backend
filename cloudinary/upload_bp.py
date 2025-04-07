from flask import jsonify , request , Blueprint , g , send_from_directory
import os
from middleware.auth_decorator import auth_required
from dotenv import load_dotenv
upload_bp = Blueprint('upload_bp' , __name__)
load_dotenv()

@upload_bp.route("/upload/<course_id>", methods=["POST"])
@auth_required
def upload(course_id):
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


    all_files = os.listdir(COURSE_SUBFOLDER)

    return jsonify({
        "message": "File uploaded successfully!!",
        "uploaded_file": file.filename,
        "all_files": all_files  # List of all files in the course folder
    }), 200

@upload_bp.route("/download/pdf/<course_id>/<file_name>" , methods=["GET"])
@auth_required
def download_pdf(course_id , file_name):
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    COURSE_SUBFOLDER = os.path.join(UPLOAD_FOLDER, str(course_id))

    file_path = os.path.join(COURSE_SUBFOLDER, file_name)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(COURSE_SUBFOLDER, file_name, as_attachment=True)
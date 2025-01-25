import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv
import os
from flask import jsonify


load_dotenv()

def upload_to_cloudinary(file_path):
    config = cloudinary.config(
        cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key = os.getenv('CLOUDINARY_API_KEY'),
        api_secret = os.getenv('CLOUDINARY_API_KEY'))
    try:
        # Upload the file to Cloudinary
        cloudinary_response = cloudinary.uploader.upload(file_path)

        # Get the URL of the uploaded file
        file_url = cloudinary_response.get('url')

        # Optionally, delete the local file after uploading to Cloudinary
        os.remove(file_path)

        return jsonify({
            "message": "File successfully uploaded to Cloudinary",
            "file_url": file_url
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to upload to Cloudinary: {str(e)}"}), 500
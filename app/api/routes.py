from flask import Blueprint, request, jsonify
from app.services.file_service import handle_file_upload
from app.services.question_service import handle_question

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/fileupload', methods=['POST'])
def file_upload():
    return handle_file_upload(request)

@api_blueprint.route('/askquestion', methods=['POST'])
def ask_question():
    return handle_question(request)
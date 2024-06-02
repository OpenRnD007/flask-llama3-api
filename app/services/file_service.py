from werkzeug.utils import secure_filename
from flask import jsonify
from app.utils.file_utils import save_file
from app.services.vectordb_service import add_file_to_vector_db

# Define the allowed file types for upload
ALLOWED_FILE_TYPES = {'pdf', 'json', 'csv'}

def handle_file_upload(request):
    """
    Handles the file upload process. It checks for the presence and validity of the 'filetype' and 'collection_name' parameter,
    verifies that a file is included in the request, and then proceeds to save the file and add its contents
    to the VectorDB.

    Args:
    request: The Flask request object containing form data and file data.

    Returns:
    A Flask response object with a JSON payload indicating success or failure.
    """
    # Check if the post request has the filetype parameter in POST data
    file_type = request.form.get('filetype')
    if not file_type or file_type.lower() not in ALLOWED_FILE_TYPES:
        return jsonify(error="Invalid or missing 'filetype' parameter. Allowed types are: pdf, json, csv."), 400

    collection_name = request.form.get('collection_name')
    if not collection_name:
        return jsonify(error="Invalid or missing 'collection_name' parameter."), 400

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    # Save the file using a utility function
    filename = secure_filename(file.filename)
    file_path = save_file(file, filename)

    # Add the file contents to the VectorDB
    return add_file_to_vector_db(file_path, file_type, collection_name)

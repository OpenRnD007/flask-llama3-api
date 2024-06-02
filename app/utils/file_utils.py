import os
from flask import current_app

def save_file(file, filename):
    """
    Saves a file to the specified upload folder.

    This function takes a file object and a filename string as arguments. It retrieves the
    upload folder path from the current application's configuration, combines it with the
    provided filename to create an absolute path, and then saves the file to that location.
    Finally, it returns the path where the file was saved.

    Args:
    file: A file object that contains the file data to be saved.
    filename: A string representing the name of the file to be saved.

    Returns:
    The absolute path to the saved file as a string.
    """
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path
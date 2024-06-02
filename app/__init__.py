from flask import Flask
from app.api.routes import api_blueprint

def create_app():
    app = Flask(__name__)

    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
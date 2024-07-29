from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .extensions.db import db
from .models.users import User

import os
from dotenv import load_dotenv
load_dotenv()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'default-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect to database
    db.init_app(app)

    with app.app_context():
        db.create_all()


    # Import Blueprint
    from app.api.auth_routes import jwt_blueprint
    from app.api.model_routes import model_blueprint

    # Limiter
    limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["50 per hour"])
    limiter.limit("10 per minute")(model_blueprint)

    # CORS
    # CORS(jwt_blueprint, resources={r"/api/auth/*": {"origins": "https://admin.backend"}})
    # CORS(model_blueprint, resources={r"/api/model/*": {"origins": "https://frontend"}})
    CORS(jwt_blueprint, resources={r"/api/auth/*": {"origins": "*"}})
    CORS(model_blueprint, resources={r"/api/model/*": {"origins": "*"}})

    # Register Blueprint
    app.register_blueprint(model_blueprint, url_prefix='/api/model')
    app.register_blueprint(jwt_blueprint, url_prefix='/api/auth')

    return app

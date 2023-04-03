from flask import Flask
from ..views import auth
from ..views import main
import os
from dotenv import load_dotenv
from ..models.database import db
from flask_cors import CORS


load_dotenv("MUSQL\env\.env")

def create_app(test_config=None):
    # Create a Flask app instance
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    CORS(app)
    
    # Configure the database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = os.environ.get('SECRET_KEY', 'fallback_key')
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Initialize the SQLAlchemy object with the Flask app
    db.init_app(app)
    app.db = db

    # Register the Blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    
    return app

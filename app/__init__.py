from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from datetime import timedelta
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    # app.config["SQLALCHEMY_ECHO"] = True
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres@localhost/morti_database"

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("RENDER_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    load_dotenv()

    #import models
    from app.models.user import User
    from app.models.message import Message
    
    #import blueprints
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from .routes.message_routes import messages_bp
    app.register_blueprint(messages_bp)

    return app
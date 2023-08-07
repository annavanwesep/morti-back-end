from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("RENDER_DATABASE_URI")
    print(f"Connected to {os.environ.get('RENDER_DATABASE_URI')}...")

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/morti_database'

    # Import models here for Alembic setup
    from app.models.user import User
    from app.models.message import Message

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    # add our google blueprint
    from app.routes.google import google_bp
    app.register_blueprint(google_bp)
    
    # add our new User blueprint
    from app.routes.user import user_bp
    app.register_blueprint(user_bp)

    # add our new Farewell Message blueprint
    from app.routes.farewell_messages import farewell_messages_bp
    app.register_blueprint(farewell_messages_bp)

    CORS(app)
    return app

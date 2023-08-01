import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
# from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.secret_key = "Morti.com"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/morti_database"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #Disable track modifications
    CORS(app)

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    load_dotenv()

    # app = Flask("Google Login for Morti")
    app.secret_key = "Morti.com"

    # Create the engine and bind it to the sessionmaker
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    Session = sessionmaker(bind=engine)

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # GOOGLE_CLIENT_ID = "444393723578-hqvu6heuhrubn9putumbq943iredeh73.apps.googleusercontent.com"
    # client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

    # flow = Flow.from_client_secrets_file(
    #     client_secrets_file=client_secrets_file, 
    #     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    #     redirect_uri="https://8218-75-172-80-33.ngrok-free.app/callback"
    #     )

    # create a fake in memory database as a Python dictionary
    fake_database = {
        "users": {},
        "save_user": lambda google_id, first_name, last_name, email: fake_database["users"].update({google_id: {"first_name": first_name, "last_name": last_name, "email": email}}),
        "get_user_by_google_id": lambda google_id: fake_database["users"].get(google_id)
    }

    def login_is_required(function):
        def wrapper(*args, **kwargs):
            if "google_id" not in session:
                return abort(401) #Authorization required
            else:
                return function()
        return wrapper

    # @app.route("/login")
    # def login():
    #     authorization_url, state = flow.authorization_url()
    #     session["state"] = state
    #     return redirect(authorization_url)

    # def save_user_to_database(id_info):
    #     google_id = id_info.get("sub")
    #     first_name = id_info.get("given_name")
    #     last_name = id_info.get("family_name")
    #     email = id_info.get("email")
        
    #     #Save user information to the fake database
    #     fake_database.save_user(google_id, first_name, last_name, email)
        
    #     #Save user information to the PostgresSQL database
    #     session = Session()
    #     user = User(google_id=google_id, first_name=first_name, last_name=last_name, email=email)
    #     session.add(user)
    #     session.commit()
    #     session.close()
        
    #     return True

    @app.route("/session", methods=["POST"])
    def session():
        print("HELLO")
        token = request.json.get("token")
        
        # Fetch the Google ID token from the request body
        if not token:
            return jsonify({"success": False, "error": "Token not provided"}), 400
        
        #Simulate token verification (implement actual)
        try: 
            id_info = id_token.verify_oauth2_token(
                id_token=token,
                request=google.auth.transport.requests.Request(),
                audience=GOOGLE_CLIENT_ID
            )    
            print(id_info)
        except ValueError:
            return jsonify({"success": False, "error": "Invalid token"}), 400
        
        flow.fetch_token(authorization_response=request.url)
        
        if not session["state"] == request.args["state"]:
            abort(500) #State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )
        
        #Save user information to the session
        
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        
        #Save user information to the database
        
        google_id = id_info.get("sub")
        first_name = id_info.get("given_name")
        last_name =id_info.get("family_name")
        email = id_info.get("email")
        
        fake_database.save_user(google_id, first_name, last_name, email)
        
        return redirect("/dashboard")
        
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")

    @app.route("/")
    def index():
        return "Hello World <a href='/login'><button>Login</button></a>"

    @app.route("/dashboard")
    @login_is_required
    def dashboard():
        #Retrieve the user's google ID from the session
        google_id = session.get("google_id")
        
        #Retrieve the user's information from the fake database
        user = fake_database.get_user_by_google_id(google_id)
        
        if user:
            #If user exists, display their information
            return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

    if __name__ == "__main__":
        app.run(debug=True)
    



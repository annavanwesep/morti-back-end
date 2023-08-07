import os
from flask import Flask, Blueprint, request, jsonify, session, abort
from google_auth_oauthlib.flow import Flow
# from .oauth_utils import get_google_user_info
from google.oauth2 import id_token
import google.auth.transport.requests
from pip._vendor import cachecontrol
from requests_oauthlib import OAuth2Session
from app.models.user import User
# from sqlalchemy import create_engine
# from sqlalchemy import sessionmaker
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

google_bp = Blueprint("google", __name__)

@google_bp.route("/google_callback", methods=["POST"])
def google_callback():
    token = request.json.get("token")

    # Fetch the Google ID token from the request body
    if not token:
        return jsonify({"success": False, "error": "Token not provided"}), 400
        
    #Simulate token verification (implement actual)
    try: 
        credentials = Flow.credentials
        print(credentials)
        # request_session = request.session()
        # cached_session = cachecontrol.CacheControl(request_session)
        # token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials.id_token,
            request=token_request,
            audience=os.environ["GOOGLE_CLIENT_ID"]
        )
        print(id_token)
    except ValueError:
        return jsonify({"success": False, "error": "Invalid token"}), 400

#         #Save user information to the session
        
#         session["google_id"] = id_info.get("sub")
#         session["name"] = id_info.get("name")
        
#         #Save user information to the database
        
#         google_id = id_info.get("sub")
#         first_name = id_info.get("given_name")
#         last_name = id_info.get("family_name")
#         email = id_info.get("email")
        
#         with conn.cursor() as cur:
#             cur.execute(
#                 "INSERT INTO users (google_id, first_name, last_name, email) "
#                 "VALUES (%s, %s, %s, %s)",
#                 (google_id, first_name, last_name, email)
#             )
#             conn.commit()        
#         client_id = ["GOOGLE_CLIENT_ID"]
#         client_secret = ["GOOGLE_CLIENT_SECRET"]
#         redirect_uri = ["RENDER_DATABASE_URI"]  # The URI to which the user will be redirected after granting permission
        
#         flow.fetch_token(authorization_response=request.url)

#         id_info = id_token.verify_oauth2_token(
#             id_token=token,
#             request=google.auth.transport.requests.Request(),
#             audience=["GOOGLE_CLIENT_ID"]
#         )    
#         print(id_info)
        
#         if not session["state"] == request.args["state"]:
#             abort(500) #State does not match!
#     except ValueError:
#         return jsonify({"success": False, "error": "Invalid token"}), 400
        
#         # flow.fetch_token(authorization_response=request.url)
        
#         # if not session["state"] == request.args["state"]:
#         #     abort(500) #State does not match!

#         # credentials = flow.credentials
#         # request_session = requests.session()
#         # cached_session = cachecontrol.CacheControl(request_session)
#         # token_request = google.auth.transport.requests.Request(session=cached_session)

#         # id_info = id_token.verify_oauth2_token(
#         #     id_token=credentials._id_token,
#         #     request=token_request,
#         #     audience=["GOOGLE_CLIENT_ID"]
#         # )
        
#         return redirect("/dashboard")
    return {}
        
        
#     def save_user_to_database(id_info):
#         google_id = id_info.get("sub")
#         first_name = id_info.get("given_name")
#         last_name =id_info.get("family_name")
#         email = id_info.get("email")
        
#         session["google_id"] = id_info.get("sub")
#         session["name"] = id_info.get("name")
                
#         #Save user to database
#         DATABASE_NAME.save_user(google_id, first_name, last_name, email)
        
#         session = Session()
#         user = User(google_id=google_id, first_name=first_name, last_name=last_name, email=email)
#         session.add(user)
#         session.commit()
#         session.close()
        
#         return True
#         # fake_database.save_user(google_id, first_name, last_name, email)


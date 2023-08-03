from flask import Blueprint, request, jsonify
from google_auth_oauthlib.flow import Flow
# from .oauth_utils import get_google_user_info
from google.oauth2 import id_token
import google.auth.transport.requests


google_bp = Blueprint("google", __name__)

@google_bp.route("/session", methods=["POST"])
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
            audience=["GOOGLE_CLIENT_ID"]
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
            audience=["GOOGLE_CLIENT_ID"]
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
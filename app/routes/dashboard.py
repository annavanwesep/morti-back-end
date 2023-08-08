from flask import Blueprint, jsonify, abort, make_response, request

dashboard_bp = Blueprint("dashboard", __name__, url_prefix=/)

@dashboard_bp.route("", methods=['GET'])
def start_app():
    return "Hello World"
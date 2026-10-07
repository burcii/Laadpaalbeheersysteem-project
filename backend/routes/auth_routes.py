from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    result, status = register_user(data)
    return jsonify(result), status

@auth_bp.route("/login", methods=["GET"])
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    result, status = login_user(email, password)
    return jsonify(result), status

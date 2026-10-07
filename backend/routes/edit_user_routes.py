from flask import Blueprint, request, jsonify
from services.edit_user_service import (
    edit_user_info_db
)

edit_user_bp = Blueprint('edit_user', __name__)


@edit_user_bp.route("/edit_user_info/<int:user_id>", methods=["PUT"])
def edit_user_info(user_id):
    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON received"}), 400

        try:
            result, status = edit_user_info_db(data, user_id)
            return jsonify(result), status
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    return jsonify({"success": False}), 500

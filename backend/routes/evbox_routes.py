from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.evbox_service import get_all_evboxes, get_active_session, get_session_history, get_evbox_info, get_dashboard_metrics, get_all_sessions, get_all_locations

evbox_bp = Blueprint("evbox", __name__)

@evbox_bp.route("/laadpalen", methods=["GET"])
def laadpalen():
    return jsonify(get_all_evboxes())

@evbox_bp.route("/laadpaal/<int:evbox_id>/active-session", methods=["GET"])
def active_session(evbox_id):
    return jsonify(get_active_session(evbox_id))

@evbox_bp.route("/laadpaal/get-sessions", methods=["GET"])
def get_sessions():
    user_id = request.args.get('user_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date') 

    if start_date and end_date:
        return jsonify(get_all_sessions(user_id, start_date, end_date))

    return jsonify(get_all_sessions(user_id))

@evbox_bp.route("/laadpaal/<int:evbox_id>/history", methods=["GET"])
def session_history(evbox_id):
    return jsonify(get_session_history(evbox_id))

@evbox_bp.route("/laadpaal/<int:evbox_id>/info", methods=["GET"])
def evbox_info(evbox_id):
    return jsonify(get_evbox_info(evbox_id))

@evbox_bp.route("/dashboard/metrics", methods=["GET"])
def dashboard_metrics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({"error": "start_date en end_date parameters zijn verplicht"}), 400
    
    result = get_dashboard_metrics(start_date, end_date)
    return jsonify(result)

@evbox_bp.route("/locaties", methods=["GET"])
def get_locations():
    return jsonify(get_all_locations())
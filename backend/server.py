from flask import Flask
from flask_cors import CORS
from flask_sock import Sock
import json
import threading
import time

from config import config
from flask_jwt_extended import JWTManager

# Import blueprints
from routes.auth_routes import auth_bp
from routes.evbox_routes import evbox_bp
from routes.user_routes import user_bp
from routes.edit_user_routes import edit_user_bp
from services.evbox_service import get_all_evboxes

app = Flask(__name__)
sock = Sock(app)
CORS(app, origins=["http://localhost", "http://127.0.0.1"])

app.config["SECRET_KEY"] = config.SECRET_KEY
jwt = JWTManager(app)
PORT = config.SERVER_PORT

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(evbox_bp)
app.register_blueprint(user_bp)
app.register_blueprint(edit_user_bp)


# --- WebSocket bridge for charger status updates ---
connections = set()


def broadcast_status(evbox_id: int, status: str):
    """
    Send a status update to all connected WebSocket clients.
    """
    payload = json.dumps({"type": "status_update", "evboxId": evbox_id, "status": status})
    stale = []
    for ws in list(connections):
        try:
            ws.send(payload)
        except Exception:
            stale.append(ws)
    for ws in stale:
        connections.discard(ws)


def poll_status_loop(interval_seconds: int = 5):
    """
    Periodically poll the database and broadcast changes.
    """
    previous_status = {}
    while True:
        try:
            evboxes = get_all_evboxes()
            if isinstance(evboxes, dict) and evboxes.get("error"):
                time.sleep(interval_seconds)
                continue
            current = {}
            for evbox in evboxes:
                evbox_id = evbox.get("EVBOXID")
                status = evbox.get("status")
                current[evbox_id] = status
                if previous_status.get(evbox_id) != status:
                    broadcast_status(evbox_id, status)
            previous_status = current
        except Exception as e:
            print(f"Error in poll_status_loop: {e}")
        time.sleep(interval_seconds)


@sock.route("/ws/chargers")
def chargers_socket(ws):
    connections.add(ws)
    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break
    finally:
        connections.discard(ws)


# Start background poller once when the module is loaded
poller_thread = threading.Thread(target=poll_status_loop, daemon=True)
poller_thread.start()


if __name__ == "__main__":
    app.run(port=PORT, debug=True)

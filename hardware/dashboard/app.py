from flask import Flask, jsonify, render_template
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from simulation.swarm_sim import SwarmCoordinator

app = Flask(__name__)
coordinator = SwarmCoordinator(num_drones=5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    drones = [{
        "id": d.id,
        "x": round(d.x, 1),
        "y": round(d.y, 1),
        "status": d.status,
        "battery": round(d.battery, 1),
        "payload": round(d.payload, 1)
    } for d in coordinator.drones]
    return jsonify({"drones": drones, "active_fires": coordinator.active_fires})

@app.route("/api/dispatch/<int:x>/<int:y>", methods=["POST"])
def dispatch(x, y):
    drone = coordinator.dispatch_nearest((x, y))
    if drone:
        return jsonify({"success": True, "drone_id": drone.id})
    return jsonify({"success": False, "message": "No available drones"}), 400

@app.route("/api/swarm/<int:x>/<int:y>", methods=["POST"])
def swarm(x, y):
    coordinator.dispatch_swarm((x, y), num=3)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

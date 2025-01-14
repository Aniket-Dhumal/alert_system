from flask import Flask, request, jsonify
from alert_system import AlertSystem  # Import your AlertSystem class

# Initialize Flask app
app = Flask(__name__)

# Initialize the alert system
alert_system = AlertSystem()

# Add a new alert
@app.route('/add_alert', methods=['POST'])
def add_alert():
    data = request.json
    try:
        alert_system.add_alert(
            alert_id=data['id'],
            interval=data['interval'],
            metric_query=data['metric_query'],
            condition_operator=data['condition_operator'],
            condition_value=data['condition_value']
        )
        return jsonify({"message": f"Alert {data['id']} added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Start the alert system
@app.route('/start', methods=['POST'])
def start_alert_system():
    try:
        alert_system.start()
        return jsonify({"message": "Alert system started!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Stop the alert system
@app.route('/stop', methods=['POST'])
def stop_alert_system():
    try:
        alert_system.stop()
        return jsonify({"message": "Alert system stopped!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get the status of the alert system
@app.route('/status', methods=['GET'])
def get_status():
    status = alert_system.get_status()
    return jsonify(status), 200

# Delete an alert
@app.route('/delete_alert/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    try:
        alert_system.delete_alert(alert_id)
        return jsonify({"message": f"Alert {alert_id} deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Main entry point for running the Flask app
if __name__ == '__main__':
    # Run Flask on 0.0.0.0 to allow external access
    app.run(host='0.0.0.0', port=80)

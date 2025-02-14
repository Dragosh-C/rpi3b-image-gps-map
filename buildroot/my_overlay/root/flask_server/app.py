from flask import Flask, request, jsonify, render_template
import json
import logging

app = Flask(__name__)

gps_data = {"latitude": None, "longitude": None}
utc_data = {"time_utc": None}

logging.basicConfig(
    filename='/root/flask_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/gps")
def get_gps():
    return jsonify(gps_data)

@app.route("/utc")
def get_utc():
    return jsonify(utc_data)

@app.route('/utc-data', methods=['POST'])
def receive_utc_data():
    global utc_data
    try:
        data = request.get_json()
        if data:
            utc_data["time_utc"] = data.get('time_utc', 'No UTC time')
            return jsonify({
                "status": "success",
                "message": "Data received successfully",
                "data": utc_data
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid data format"
            }), 400
    except Exception as e:
        logging.error(f"Error receiving UTC data: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/gps-data', methods=['POST'])
def receive_gps_data():
    global gps_data
    try:
        data = request.get_json()
        if data:
            gps_data["latitude"] = data.get('latitude', 'No latitude')
            gps_data["longitude"] = data.get('longitude', 'No longitude')
            
            return jsonify({
                "status": "success",
                "message": "Data received successfully",
                "data": gps_data
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid data format"
            }), 400
    except Exception as e:
        logging.error(f"Error receiving GPS data: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/get-gps', methods=['GET'])
def get_gps_data():
    return jsonify(gps_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)


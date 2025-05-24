from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from nws_api import get_high_wind_period  # or whatever other logic module
import os

load_dotenv()
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend (Vite)

@app.route("/api/windbot", methods=["POST"])
def windbot():
    data = request.get_json()
    cmd = data.get("command", "").lower().strip()

    lat = os.getenv("LAT")
    lon = os.getenv("LON")
    threshold = float(os.getenv("WIND_THRESHOLD", 25))

    if cmd == "forecast" or cmd == "wind now":
        message = get_high_wind_period(lat, lon, threshold)
    elif cmd == "hello":
        message = "👋 Hello! You are connected to Jamison's command center."
    else:
        message = "🤖 Unknown command. Try 'forecast' or 'hello'."

    return jsonify({"message": message})


if __name__ == "__main__":
    app.run(debug=True)

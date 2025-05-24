from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from nws_api import handle_weather_command # or whatever other logic module
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

    if cmd == "hello":
        message = "👋 Hello! You are connected to Jamison's command center."
    elif cmd == "commands":
        message = (
            "📋 Available commands:\n"
            "- hello\n"
            "- commands\n"
            "- forecast\n"
            "- wind now\n"
            "- temp now\n"
            "- rain today\n"
            "- alert\n"
            "- hourly\n"
            "- sunrise\n"
            "- sunset"
        )
    elif cmd in [
        "forecast", "wind now", "temp now", "rain today",
        "alert", "hourly", "sunrise", "sunset"
    ]:
        message = handle_weather_command(cmd, lat, lon)
    else:
        message = "🤖 Unknown command. Type 'commands' to see what's available."

    return jsonify({"message": message})


if __name__ == "__main__":
    app.run(debug=True)

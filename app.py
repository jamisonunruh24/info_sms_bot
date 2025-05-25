from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from nws_api import handle_weather_command # or whatever other logic module
import os
from memory import load_memory, save_memory


load_dotenv()
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend (Vite)

import requests

@app.route("/api/vape", methods=["POST"])
def vapebot():
    data = request.get_json()
    prompt = data.get("command", "").strip()
    print("🔥 Prompt received:", prompt)

    try:
        history = load_memory()
        MAX_CONTEXT = 8
        if len(history) > MAX_CONTEXT:
            history = history[-MAX_CONTEXT:]

        history.append({"role": "user", "content": prompt})

        r = requests.post("http://localhost:11434/api/chat", json={
            "model": "mistral",
            "messages": history,
            "stream": False
        })

        data = r.json()
        print("🧠 Raw LLM response:", data)

        reply = data.get("message", {}).get("content")
        if not reply:
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "🤖 No response.")

        history.append({"role": "assistant", "content": reply})
        save_memory(history)

        return jsonify({"message": reply})
    except Exception as e:
        print("❌ LLM error:", e)
        return jsonify({"message": f"❌ Could not process: {str(e)}"}), 500




if __name__ == "__main__":
    app.run(debug=True)

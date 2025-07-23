import os # Import the 'os' module to access environment variables
from flask import Flask, jsonify
from flask_cors import CORS # Import CORS to handle cross-origin requests
import json

app = Flask(__name__)

# Initialize CORS for your app.
# IMPORTANT: For production, you should restrict this to your frontend's specific URL
# For example: CORS(app, origins="https://your-frontend-url.onrender.com")
# For now, we'll allow all origins for easier testing.
CORS(app)

# Utility function to read JSON files
# Ensure that your JSON files (speaker_feedback.json, team_summary.json, etc.)
# are located in a 'data' subfolder relative to your app.py file.
def load_json(filename):
    # Using os.path.join for better path handling across different OS
    # and to ensure it looks for 'data' relative to the current script.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", filename)
    with open(file_path, "r") as file:
        return json.load(file)

@app.route("/")
def index():
    # A simple route to confirm the backend is running
    return "🎙️ TabbyCat AI Companion Backend is Running!"

@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    return jsonify(data)

@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    return jsonify(data)

@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    return jsonify(data)

@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    return jsonify(data)

if __name__ == "__main__":
    # Get the port from environment variables provided by Render,
    # or default to 5000 for local development.
    port = int(os.environ.get("PORT", 5000))

    # For production, debug should be False.
    # When deploying with Gunicorn (which we'll use on Render),
    # Gunicorn handles the server, so app.run() is primarily for local testing.
    app.run(debug=False, host='0.0.0.0', port=port)

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path

# Initialize the Flask app with the correct template and static folders
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Use Path for platform-independent path handling
DATA_FOLDER = Path('data')

# Utility function to load JSON files
def load_json(filename):
    try:
        with open(DATA_FOLDER / filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'.")
        return None

# 🔹 Serve Frontend UI
@app.route("/")
def index():
    return render_template("index.html")

# 🔹 NEW API Route: Serve static data files with no caching
@app.route("/static/data/<path:filename>")
def get_data(filename):
    """
    Serves the data files directly from the 'data' directory
    and adds a 'Cache-Control' header to prevent browser caching.
    """
    try:
        response = send_from_directory(DATA_FOLDER, filename, as_attachment=False)
        # This is the crucial part that forces the browser to re-download the file every time
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    except FileNotFoundError:
        return jsonify({"error": f"File '{filename}' not found."}), 404

# Your existing API routes for AI integration can remain as they are
# as they are not affected by this change.

# 🔹 API Route: Get speaker feedback
@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    if data is None:
        return jsonify({"error": "Speaker feedback data could not be loaded."}), 500
    return jsonify(data)

# 🔹 API Route: Get team summaries
@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    if data is None:
        return jsonify({"error": "Team summary data could not be loaded."}), 500
    return jsonify(data)

# 🔹 API Route: Get judge insights
@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    if data is None:
        return jsonify({"error": "Judge insights data could not be loaded."}), 500
    return jsonify(data)

# 🔹 API Route: Get motions
@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    if data is None:
        return jsonify({"error": "Motion data could not be loaded."}), 500
    return jsonify(data)

# This block is for local development only. Render will use a WSGI server like Gunicorn.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

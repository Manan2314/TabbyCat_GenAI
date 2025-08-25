import os
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import json

# 🔹 Import AIIntegration class
from ai_integration import AIIntegration

# Ensure correct absolute paths (important for Render + Replit)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Make sure data folder exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)
CORS(app)  # Allow CORS for frontend

# 🔹 Initialize AI processor
ai_processor = AIIntegration()

# ---------------- Utility ----------------
def load_json(filename):
    file_path = os.path.join(DATA_DIR, filename)
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"❌ Error: '{filename}' not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Error: Could not parse JSON in '{filename}'")
        return None

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Corrected route to match the frontend request from /static/data
@app.route("/static/data/<path:filename>")
def serve_data(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    if data is None:
        return jsonify({"error": "Speaker feedback data not found"}), 500

    processed_speakers = []
    data_to_process = data if isinstance(data, list) else [data]

    for speaker_item in data_to_process:
        insights = ai_processor.generate_speaker_feedback(speaker_item)
        combined_item = speaker_item.copy()
        combined_item['ai_insights'] = insights
        processed_speakers.append(combined_item)

    return jsonify(processed_speakers)

@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    if data is None:
        return jsonify({"error": "Team summary data not found"}), 500

    processed = []
    data_to_process = data if isinstance(data, list) else [data]

    for team_item in data_to_process:
        insights = ai_processor.generate_team_insights_realtime(team_item)
        combined = team_item.copy()
        combined["ai_insights"] = insights
        processed.append(combined)

    return jsonify(processed)

@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    if data is None:
        return jsonify({"error": "Judge insights data not found"}), 500

    insights = ai_processor.analyze_judge_comprehensive(data)
    processed_judge_data = data.copy()
    processed_judge_data['ai_insights'] = insights
    return jsonify(processed_judge_data)

@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    if data is None:
        return jsonify({"error": "Motion data not found"}), 500
    return jsonify(data)

# ---------------- Run App ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets $PORT
    app.run(debug=False, host="0.0.0.0", port=port)

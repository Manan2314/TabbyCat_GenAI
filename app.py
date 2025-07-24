import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# 🔹 Import your AI processing logic
from ai_integration import generate_speaker_insights, generate_team_insights, generate_judge_insights

app = Flask(__name__)
CORS(app)

# Utility function to load JSON files
def load_json(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", filename)
    with open(file_path, "r") as file:
        return json.load(file)

@app.route("/")
def index():
    return "🎙️ TabbyCat AI Companion Backend is Running!"

@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    insights = generate_speaker_insights(data)
    return jsonify({"raw": data, "insights": insights})

@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    insights = generate_team_insights(data)
    return jsonify({"raw": data, "insights": insights})

@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    insights = generate_judge_insights(data)
    return jsonify({"raw": data, "insights": insights})

@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

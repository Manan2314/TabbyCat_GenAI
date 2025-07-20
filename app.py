from flask import Flask, jsonify
import json

app = Flask(__name__)

# Utility function to read JSON files
def load_json(filename):
    with open(f"data/{filename}", "r") as file:
        return json.load(file)

@app.route("/")
def index():
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
    app.run(debug=True)
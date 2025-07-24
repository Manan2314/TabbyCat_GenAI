import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

def load_json(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", filename)
    with open(file_path, "r") as file:
        return json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

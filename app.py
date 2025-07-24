import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

# 🔹 Correct Import: Import the AIIntegration CLASS
from ai_integration import AIIntegration

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 🔹 Initialize an instance of your AIIntegration class
ai_processor = AIIntegration()

# Utility function to load JSON files
def load_json(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")  # Assuming 'data' subdirectory
    file_path = os.path.join(data_dir, filename)

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at: {data_dir}")

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file '{filename}' not found at {file_path}.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'.")
        return None

# 🔹 Serve Frontend UI
@app.route("/")
def index():
    return render_template("index.html")  # Loads the main HTML UI

# 🔹 API Route: Get speaker feedback
@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    if data is None:
        return jsonify({"error": "Speaker feedback data could not be loaded."}), 500

    all_speaker_insights = []
    if isinstance(data, list):
        for speaker_item in data:
            insights = ai_processor.generate_speaker_feedback(speaker_item)
            all_speaker_insights.append({"speaker_data": speaker_item, "insights": insights})
    else:
        insights = ai_processor.generate_speaker_feedback(data)
        all_speaker_insights.append({"speaker_data": data, "insights": insights})

    return jsonify({"raw": data, "insights": all_speaker_insights})

# 🔹 API Route: Get team summaries
@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    if data is None:
        return jsonify({"error": "Team summary data could not be loaded."}), 500

    insights = ai_processor.generate_team_insights_realtime(data)
    return jsonify({"raw": data, "insights": insights})

# 🔹 API Route: Get judge insights
@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    if data is None:
        return jsonify({"error": "Judge insights data could not be loaded."}), 500

    insights = ai_processor.analyze_judge_comprehensive(data)
    return jsonify({"raw": data, "insights": insights})

# 🔹 API Route: Get motions
@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    if data is None:
        return jsonify({"error": "Motion data could not be loaded."}), 500

    return jsonify(data)

# 🔹 Start the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

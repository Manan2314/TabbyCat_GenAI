import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

# 🔹 Correct Import: Import the AIIntegration CLASS
# You no longer import individual functions directly.
from ai_integration import AIIntegration

app = Flask(__name__)
CORS(app)

# 🔹 Initialize an instance of your AIIntegration class
ai_processor = AIIntegration()

# Utility function to load JSON files
def load_json(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data") # Assuming 'data' subdirectory
    file_path = os.path.join(data_dir, filename)
    
    # Optional: Create 'data' directory if it doesn't exist (useful for local setup)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at: {data_dir}")

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Data file '{filename}' not found at {file_path}. Please ensure it exists.")
        return None # Return None to indicate failure
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'. Please check its format.")
        return None # Return None to indicate failure

@app.route("/")
def index():
    return "🎙️ TabbyCat AI Companion Backend is Running!"

@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    if data is None:
        return jsonify({"error": "Speaker feedback data could not be loaded or found."}), 500

    all_speaker_insights = []
    # Check if 'data' is a list (e.g., [speaker1_data, speaker2_data])
    if isinstance(data, list):
        for speaker_item in data:
            # Call generate_speaker_feedback for each speaker in the list
            # ai_integration's generate_speaker_feedback expects a single speaker's dict
            insights = ai_processor.generate_speaker_feedback(speaker_item)
            all_speaker_insights.append({"speaker_data": speaker_item, "insights": insights})
    else:
        # If 'data' is a single dictionary (e.g., for one speaker)
        insights = ai_processor.generate_speaker_feedback(data)
        all_speaker_insights.append({"speaker_data": data, "insights": insights})

    return jsonify({"raw": data, "insights": all_speaker_insights})

@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    if data is None:
        return jsonify({"error": "Team summary data could not be loaded or found."}), 500
    
    # 🔹 Use the correct method name from AIIntegration: generate_team_insights_realtime
    # Assuming team_summary.json contains the data for a single team.
    insights = ai_processor.generate_team_insights_realtime(data)
    return jsonify({"raw": data, "insights": insights})

@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    if data is None:
        return jsonify({"error": "Judge insights data could not be loaded or found."}), 500
        
    # 🔹 Use the correct method name from AIIntegration: analyze_judge_comprehensive
    # Assuming judge_insights.json contains the data for a single judge.
    insights = ai_processor.analyze_judge_comprehensive(data)
    return jsonify({"raw": data, "insights": insights})

@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    if data is None:
        return jsonify({"error": "Motion data could not be loaded or found."}), 500
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

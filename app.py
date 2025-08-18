import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

# 🔹 Correct Import: Import the AIIntegration CLASS
from ai_integration import AIIntegration

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app) # Ensure CORS is enabled for all origins for development, or specify your frontend origin

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
        print(f"Error: Could not decode JSON from '{filename}'. Please check its format.")
        return None

# 🔹 Serve Frontend UI
@app.route("/")
def index():
    return render_template("index.html")  # Loads the main HTML UI

# 🔹 API Route: Get speaker feedback
@app.route("/speakers", methods=["GET"])
def get_speakers():
    # speaker_feedback.json is an array of speaker round data
    data = load_json("speaker_feedback.json")
    if data is None:
        return jsonify({"error": "Speaker feedback data could not be loaded."}), 500

    processed_speakers = []

    # Ensure `data_list` always holds an iterable for the loop
    # Your speaker_feedback.json is an array, so this will correctly treat `data` as a list.
    # If it were ever a single object, this handles it gracefully.
    data_to_process = data if isinstance(data, list) else [data]

    for speaker_item in data_to_process: # Loop through each individual speaker entry (round data)
        # Generate AI insights for each speaker item (round performance)
        # ai_processor.generate_speaker_feedback expects a single speaker_data dict
        insights = ai_processor.generate_speaker_feedback(speaker_item)

        # Combine the original speaker_item with its AI insights
        # This creates a new dictionary for each round's speaker data + its insights
        combined_item = speaker_item.copy() # Make a copy to avoid modifying original loaded data
        combined_item['ai_insights'] = insights # Add AI insights under a new key
        processed_speakers.append(combined_item)

    # 🔹 Return the list of processed speaker items directly
    return jsonify(processed_speakers)

# 🔹 API Route: Get team summaries
@app.route("/teams", methods=["GET"])
def get_teams():
    # team_summary.json is a single object
    data = load_json("team_summary.json")
    if data is None:
        return jsonify({"error": "Team summary data could not be loaded."}), 500

    # Generate AI insights for the entire team summary object
    # ai_processor.generate_team_insights_realtime expects a single team_data object
    insights = ai_processor.generate_team_insights_realtime(data)

    # 🔹 Add AI insights directly to the team data object
    # Make a copy to avoid modifying the original loaded data if it's used elsewhere
    processed_team_data = data.copy()
    processed_team_data['ai_insights'] = insights

    # 🔹 Return the processed team data object directly
    return jsonify(processed_team_data)

# 🔹 API Route: Get judge insights
@app.route("/judges", methods=["GET"])
def get_judges():
    # judge_insights.json is a single object
    data = load_json("judge_insights.json")
    if data is None:
        return jsonify({"error": "Judge insights data could not be loaded."}), 500

    # Generate AI insights for the entire judge insights object
    # ai_processor.analyze_judge_comprehensive expects a single judge_data object
    insights = ai_processor.analyze_judge_comprehensive(data)

    # 🔹 Add AI insights directly to the judge data object
    # Make a copy to avoid modifying the original loaded data if it's used elsewhere
    processed_judge_data = data.copy()
    processed_judge_data['ai_insights'] = insights

    # 🔹 Return the processed judge data object directly
    return jsonify(processed_judge_data)

# 🔹 API Route: Get motions
@app.route("/motions", methods=["GET"])
def get_motions():
    # motion_data.json is an array of objects
    data = load_json("motion_data.json")
    if data is None:
        return jsonify({"error": "Motion data could not be loaded."}), 500

    # 🔹 Return the motion data directly (it's already an array)
    return jsonify(data)

# 🔹 Start the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

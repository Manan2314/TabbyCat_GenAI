from flask import Flask, jsonify, send_from_directory, request
import json
from app import app
import os

# ---------------------------
# Flask app setup
# ---------------------------
app = Flask(__name__, static_folder='.', static_url_path='')

# Base directory for data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# ---------------------------
# Utility function to read JSON
# ---------------------------
def load_json(filename):
    file_path = os.path.join(DATA_DIR, filename)
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": f"{filename} not found"}
    except json.JSONDecodeError:
        return {"error": f"{filename} is not valid JSON"}

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/api")
def api_status():
    return "TabbyCat AI Companion Backend is Running!"

@app.route("/speakers", methods=["GET"])
def get_speakers():
    return jsonify(load_json("speaker_feedback.json"))

@app.route("/teams", methods=["GET"])
def get_teams():
    return jsonify(load_json("team_summary.json"))

@app.route("/motions", methods=["GET"])
def get_motions():
    return jsonify(load_json("motion_data.json"))

@app.route("/judges", methods=["GET"])
def get_judges():
    return jsonify(load_json("judge_insights.json"))

# ---------------------------
# AI Integration using Gemini
# ---------------------------
import google.generativeai as genai

# Load Gemini API key from env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Pick a Gemini model
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def gemini_generate(prompt: str):
    """Helper to query Gemini safely."""
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini error: {str(e)}"

@app.route("/ai/analyze-speaker", methods=["POST"])
def ai_analyze_speaker():
    data = request.get_json()
    speaker_name = data.get("speaker_name", "Speaker")
    scores = data.get("scores", [])
    motion = data.get("motion", "")

    prompt = f"""
    Analyze the performance of {speaker_name}.
    Scores: {scores}
    Motion debated: "{motion}"
    Provide constructive feedback and improvement tips.
    """
    insights = gemini_generate(prompt)
    return jsonify({
        "status": "success",
        "insights": insights,
        "speaker": speaker_name,
        "ai_powered": True
    })

@app.route("/ai/motion-strategy", methods=["POST"])
def ai_motion_strategy():
    data = request.get_json()
    motion = data.get("motion", "")
    side = data.get("side", "Government")
    team_strengths = data.get("team_strengths", [])

    prompt = f"""
    Debate motion: "{motion}"
    Side: {side}
    Team strengths: {team_strengths}
    Suggest a strong strategy with arguments, counter-arguments, and style tips.
    """
    strategy = gemini_generate(prompt)
    return jsonify({
        "status": "success",
        "strategy": strategy,
        "motion": motion,
        "side": side,
        "ai_powered": True
    })

@app.route("/ai/judge-insights", methods=["POST"])
def ai_judge_insights():
    data = request.get_json()
    judge_history = data.get("judge_history", {})

    prompt = f"""
    Judge history: {judge_history}
    Analyze judging patterns, possible biases, and preferred debating style.
    """
    insights = gemini_generate(prompt)
    return jsonify({
        "status": "success",
        "insights": insights,
        "ai_powered": True
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "ai_integration": "Gemini ready",
        "analytics_libraries": ["matplotlib", "seaborn", "plotly", "pandas", "numpy"],
        "supported_apis": ["Gemini", "OpenAI (optional)"]
    })

# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    # Render provides a PORT env variable, fallback to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

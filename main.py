from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

# Import the AIIntegration class
from ai_integration import AIIntegration

# Initialize the Flask app with the correct template folder
app = Flask(__name__, template_folder='templates')
CORS(app)

# Initialize an instance of your AIIntegration class
ai_processor = AIIntegration()

# Utility function to load JSON files
def load_json(filename):
    # This path is now relative to the project root, and the case is correct
    try:
        with open(f"data/{filename}", "r") as file:
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
    # This now correctly serves index.html from the 'templates' folder
    return render_template("index.html")

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

# All AI Integration endpoints
@app.route("/ai/analyze-speaker", methods=["POST"])
def ai_analyze_speaker():
    try:
        data = request.get_json()
        speaker_name = data.get('speaker_name', 'Speaker')
        scores = data.get('scores', [])
        motion = data.get('motion', '')
        
        insights = ai_processor.generate_real_time_speaker_insights(
            speaker_name, scores, motion
        )
        
        return jsonify({
            "status": "success",
            "insights": insights,
            "speaker": speaker_name,
            "ai_powered": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/ai/motion-strategy", methods=["POST"])
def ai_motion_strategy():
    try:
        data = request.get_json()
        motion = data.get('motion', '')
        side = data.get('side', 'Government')
        team_strengths = data.get('team_strengths', [])
        
        strategy = ai_processor.generate_motion_strategy_realtime(
            motion, side, team_strengths
        )
        
        return jsonify({
            "status": "success",
            "strategy": strategy,
            "motion": motion,
            "side": side,
            "ai_powered": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/ai/judge-insights", methods=["POST"])
def ai_judge_insights():
    try:
        data = request.get_json()
        judge_history = data.get('judge_history', {})
        
        insights = ai_processor.analyze_judge_patterns_realtime(judge_history)
        
        return jsonify({
            "status": "success",
            "insights": insights,
            "ai_powered": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/ai/team-insights", methods=["POST"])
def ai_team_insights():
    try:
        data = request.get_json()
        team_data = data.get('team_data', {})
        
        insights = ai_processor.generate_team_insights_realtime(team_data)
        
        return jsonify({
            "status": "success",
            "insights": insights,
            "team": team_data.get('team_name', 'Unknown'),
            "ai_powered": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/ai/judge-comprehensive", methods=["POST"])
def ai_judge_comprehensive():
    try:
        data = request.get_json()
        judge_data = data.get('judge_data', {})
        
        insights = ai_processor.analyze_judge_comprehensive(judge_data)
        
        return jsonify({
            "status": "success",
            "insights": insights,
            "judge": judge_data.get('judge_name', 'Unknown'),
            "ai_powered": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/ai/performance-report", methods=["POST"])
def ai_performance_report():
    try:
        data = request.get_json()
        speaker_data_list = data.get('speaker_data', [])
        
        report_b64 = ai_processor.generate_performance_report(speaker_data_list)
        
        return jsonify({
            "status": "success",
            "report_chart": report_b64,
            "analytics_powered": True
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/ai/speaker-analytics", methods=["POST"])
def ai_speaker_detailed_analytics():
    try:
        data = request.get_json()
        speaker_name = data.get('speaker_name', 'Speaker')
        scores = data.get('scores', [])
        
        analytics = ai_processor._generate_speaker_analytics(speaker_name, scores)
        visualizations = ai_processor._create_speaker_visualizations(scores, speaker_name)
        
        return jsonify({
            "status": "success",
            "analytics": analytics,
            "visualizations": visualizations,
            "speaker": speaker_name
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "ai_integration": "ready",
        "analytics_libraries": ["matplotlib", "seaborn", "plotly", "pandas", "numpy"],
        "supported_apis": ["OpenAI", "Sarvam AI", "Custom Models"]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

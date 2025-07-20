
from flask import Flask, jsonify, send_from_directory
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Utility function to read JSON files
def load_json(filename):
    with open(f"Data/{filename}", "r") as file:
        return json.load(file)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/api")
def api_status():
    return "TabbyCat AI Companion Backend is Running!"

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

# AI Integration endpoints with Sarvam AI
from ai_integration import AIIntegration
from flask import request

ai_integration = AIIntegration()

@app.route("/ai/analyze-speaker", methods=["POST"])
def ai_analyze_speaker():
    try:
        data = request.get_json()
        speaker_name = data.get('speaker_name', 'Speaker')
        scores = data.get('scores', [])
        motion = data.get('motion', '')
        
        insights = ai_integration.generate_real_time_speaker_insights(
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
        
        strategy = ai_integration.generate_motion_strategy_realtime(
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
        
        insights = ai_integration.analyze_judge_patterns_realtime(judge_history)
        
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
        
        insights = ai_integration.generate_team_insights_realtime(team_data)
        
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
        
        insights = ai_integration.analyze_judge_comprehensive(judge_data)
        
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
        
        report_b64 = ai_integration.generate_performance_report(speaker_data_list)
        
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
        
        analytics = ai_integration._generate_speaker_analytics(speaker_name, scores)
        visualizations = ai_integration._create_speaker_visualizations(scores, speaker_name)
        
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
    app.run(host='0.0.0.0', port=5000, debug=True)

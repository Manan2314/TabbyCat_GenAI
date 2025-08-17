import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

from ai_integration import AIIntegration

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
ai_processor = AIIntegration()

# ---------- utilities ----------
def load_json(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    file_path = os.path.join(data_dir, filename)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory at: {data_dir}")
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Data file not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Bad JSON in: {file_path}")
        return None

# ---------- routes ----------
@app.route("/")
def index():
    # if you have templates/index.html
    try:
        return render_template("index.html")
    except Exception:
        return "🎙️ TabbyCat AI Companion Backend is Running!"

@app.route("/speakers", methods=["GET"])
def get_speakers():
    data = load_json("speaker_feedback.json")
    if data is None:
        return jsonify({"error": "Speaker feedback not found."}), 500

    insights_list = []
    if isinstance(data, list):
        for item in data:
            insights = ai_processor.generate_speaker_feedback(item)
            insights_list.append({"speaker_data": item, "insights": insights})
    else:
        insights = ai_processor.generate_speaker_feedback(data)
        insights_list.append({"speaker_data": data, "insights": insights})

    return jsonify({"raw": data, "insights": insights_list})

@app.route("/teams", methods=["GET"])
def get_teams():
    data = load_json("team_summary.json")
    if data is None:
        return jsonify({"error": "Team summary not found."}), 500
    # keep existing realtime method output shape
    insights = ai_processor.build_round_report(
        team_data=data,
        speaker_list=load_json("speaker_feedback.json") if load_json("speaker_feedback.json") else [],
        judge_data=load_json("judge_insights.json") if load_json("judge_insights.json") else {},
        motion=(load_json("motion_data.json") or {}).get("motion",""),
        side=(load_json("motion_data.json") or {}).get("predicted_side","")
    )
    return jsonify({"raw": data, "report": insights})

@app.route("/judges", methods=["GET"])
def get_judges():
    data = load_json("judge_insights.json")
    if data is None:
        return jsonify({"error": "Judge insights not found."}), 500
    guide = ai_processor.build_judge_adaptation_guide(data)
    return jsonify({"raw": data, "guide": guide})

@app.route("/motions", methods=["GET"])
def get_motions():
    data = load_json("motion_data.json")
    if data is None:
        return jsonify({"error": "Motion data not found."}), 500
    return jsonify(data)

# ---------- NEW: motion → strategy ----------
@app.route("/motion/strategy", methods=["GET"])
def motion_strategy():
    # Accept query params or fallback to data file
    motion = request.args.get("motion")
    side = request.args.get("side")
    motion_json = load_json("motion_data.json") or {}
    if not motion:
        motion = motion_json.get("motion") or motion_json.get("title") or "This House..."
    if not side:
        side = motion_json.get("predicted_side") or "Government"
    strategy = ai_processor.generate_motion_strategy(motion, side, motion_meta=motion_json)
    return jsonify({"motion": motion, "side": side, "strategy": strategy})

# ---------- NEW: one-click Round Report ----------
@app.route("/report", methods=["GET"])
def round_report():
    team = load_json("team_summary.json") or {}
    speakers = load_json("speaker_feedback.json") or []
    judge = load_json("judge_insights.json") or {}
    motion_data = load_json("motion_data.json") or {}
    motion = motion_data.get("motion") or motion_data.get("title") or ""
    side = motion_data.get("predicted_side") or ""
    report = ai_processor.build_round_report(team, speakers, judge, motion, side)
    return jsonify({"report": report})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

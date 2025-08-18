from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------------- Dummy AI Logic ----------------
# Replace these with your Sarvam AI API calls later
def analyze_team(data):
    return {"insight": f"✅ Team Analysis: {data}"}

def analyze_speaker(data):
    return {"insight": f"✅ Speaker Analysis: {data}"}

def analyze_judge(data):
    return {"insight": f"✅ Judge Analysis: {data}"}

def analyze_motion(data):
    return {"insight": f"✅ Motion Analysis: Debate motion '{data}' analyzed."}

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/team-analysis", methods=["POST"])
def team_analysis():
    try:
        data = request.json.get("text", "")
        return jsonify(analyze_team(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/speaker-analysis", methods=["POST"])
def speaker_analysis():
    try:
        data = request.json.get("text", "")
        return jsonify(analyze_speaker(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/judge-analysis", methods=["POST"])
def judge_analysis():
    try:
        data = request.json.get("text", "")
        return jsonify(analyze_judge(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/motion-analysis", methods=["POST"])
def motion_analysis():
    try:
        data = request.json.get("text", "")
        return jsonify(analyze_motion(data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- Run App ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

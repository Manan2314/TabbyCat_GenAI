import os
import json
from flask import Flask, render_template, send_from_directory, jsonify

# Initialize Flask with explicit static and template folders
app = Flask(__name__, static_folder="static", template_folder="templates")

# -----------------------------
# Root route → renders index.html
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -----------------------------
# Static file route (kept for safety, though Flask can serve automatically)
# -----------------------------
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# -----------------------------
# Route to serve JSON data files from /data folder
# -----------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@app.route('/data/<filename>')
def get_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "File not found"}), 404

# -----------------------------
# Main entry point
# -----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)


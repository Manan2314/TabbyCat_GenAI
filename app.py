# Import necessary modules from the Flask framework
from flask import Flask, render_template, send_from_directory

# This is the standard way to initialize a Flask application.
# The static_url_path parameter explicitly tells Flask to serve files from the
# 'static' folder when a URL like '/static/style.css' is requested.
app = Flask(__name__, static_url_path='/static')

# Define a route for the root URL of your application ('/').
# This route will render your main HTML file.
@app.route('/')
def index():
    # The render_template function looks for 'index.html' inside a 'templates' folder.
    # Make sure your 'index.html' file is located there.
    return render_template('index.html')

# This is an optional but robust route to ensure static files are served correctly.
@app.route('/static/<path:filename>')
def serve_static(filename):
    # This function tells the server to find the requested 'filename'
    # inside the 'static' directory and serve it back to the browser.
    return send_from_directory('static', filename)

from flask import Flask, request
import os
import sys

# allow python to access project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gui.pipeline_runner import run_full_pipeline

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"


@app.route("/")
def home():
    return '''
    <h2>Deepfake Detection System (Pipeline Execution)</h2>

    <form method="POST" action="/run_pipeline" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <br><br>
        <input type="submit" value="Run Full Pipeline">
    </form>
    '''


@app.route("/run_pipeline", methods=["POST"])
def run_pipeline():
    file = request.files["file"]

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)

    results = run_full_pipeline(video_path)

    return f"""
    <h3>Pipeline Execution Result</h3>
    <pre>{results}</pre>
    """


if __name__ == "__main__":
    app.run(debug=True)


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.makedirs("uploads", exist_ok=True)

from flask import Flask, request
from gui.pipeline_runner import run_full_pipeline


from gui.pipeline_runner import run_full_pipeline

app = Flask(__name__)

UPLOAD_FOLDER = "video_inputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return """
    <h2>Deepfake Detection System (Phase-2)</h2>
    <form method="POST" action="/analyze" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <br><br>
        <button type="submit">Run Detection</button>
    </form>
    """


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    result = run_full_pipeline(save_path)

    return f"""
    <h3>Result</h3>
    <pre>{result}</pre>
    <a href="/">Analyze another video</a>
    """


if __name__ == "__main__":
    app.run(debug=True)

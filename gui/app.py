from flask import Flask, render_template, request
import os

from gui.pipeline_runner import run_full_pipeline

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "video" not in request.files:
        return render_template(
            "result.html",
            result={"status": "No video uploaded", "error": "File missing"}
        )

    file = request.files["video"]

    if file.filename == "":
        return render_template(
            "result.html",
            result={"status": "No video selected", "error": ""}
        )

    if not file.filename.lower().endswith(".mp4"):
        return render_template(
            "result.html",
            result={"status": "Invalid file", "error": "Only MP4 allowed"}
        )

    video_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(video_path)

    result = run_full_pipeline(video_path)

    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


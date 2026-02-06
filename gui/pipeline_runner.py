import os
import traceback
import subprocess


def run_full_pipeline(video_path):
    """
    Executes the COMPLETE deepfake detection pipeline:
    Video -> Audio -> Logic
    (all as scripts)
    """

    results = {
        "video": "Not executed",
        "audio": "Not executed",
        "logic": "Not executed",
        "error": None
    }

    try:
        # ---------- BASIC CHECK ----------
        if not os.path.exists(video_path):
            raise FileNotFoundError("Uploaded file not found")

        if not video_path.lower().endswith(".mp4"):
            raise ValueError("Only MP4 videos are supported")

        # ---------- VIDEO PIPELINE ----------
        subprocess.run(
            ["python", "video_module/video_experiments.py", video_path],
            check=True
        )
        results["video"] = "Video pipeline executed"

        # ---------- AUDIO PIPELINE ----------
        subprocess.run(
            ["python", "audio_module/audio_experiments.py", video_path],
            check=True
        )
        results["audio"] = "Audio pipeline executed"

        # ---------- LOGIC PIPELINE ----------
        subprocess.run(
            ["python", "logic/rule_based_classifier.py"],
            check=True
        )
        results["logic"] = "Logic pipeline executed"

        return results

    except Exception as e:
        results["error"] = str(e)
        results["trace"] = traceback.format_exc()
        return results

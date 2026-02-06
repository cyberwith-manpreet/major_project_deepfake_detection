from video_module.video_experiments import process_single_video
from audio_module.audio_experiments import process_single_video as process_audio
from logic.rule_based_classifier import run_classifier


def run_full_pipeline(video_path):
    try:
        # VIDEO PIPELINE
        motion_array = process_single_video(video_path)
        video_motion_length = len(motion_array)

        # AUDIO PIPELINE
        audio_result = process_audio(video_path)
        audio_silence_points = audio_result["silence_points"]

        # LOGIC
        mismatch_score = abs(video_motion_length - audio_silence_points) / max(
            video_motion_length, audio_silence_points
        )

        final_decision = run_classifier(mismatch_score)

        return {
            "video_motion_length": video_motion_length,
            "audio_silence_points": audio_silence_points,
            "mismatch_score": round(mismatch_score, 4),
            "final_decision": final_decision
        }

    except Exception as e:
        return {
            "status": "Video pipeline failed",
            "error": str(e)
        }

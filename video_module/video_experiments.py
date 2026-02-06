import os
import sys

from video_module.videoreader import VideoReader
from video_module.frame_extractor import extract_frames
from video_module.frame_preprocessing import preprocess_frames
from video_module.motion_calculator import calculate_motion_array


def process_single_video(video_path):
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not video_path.lower().endswith(".mp4"):
        raise ValueError("Only .mp4 videos are supported")

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    extracted_dir = os.path.join("extracted_frames", video_name)
    preprocessed_dir = os.path.join("preprocessed_frames", video_name)

    os.makedirs(extracted_dir, exist_ok=True)
    os.makedirs(preprocessed_dir, exist_ok=True)

    video = VideoReader(video_path)
    if not video.open_video():
        raise RuntimeError("❌ Error opening video file")

    props = video.get_video_properties()
    video.release()

    print(f"\n🎥 Processing video: {video_name}")
    print(
        f"Frames: {props['total_frames']} | "
        f"FPS: {props['fps']:.2f} | "
        f"Duration: {props['duration_seconds']:.2f} seconds"
    )

    extract_frames(video_path, extracted_dir)
    preprocess_frames(extracted_dir, preprocessed_dir)

    motion = calculate_motion_array(preprocessed_dir)
    print(f"✅ Motion array length: {len(motion)}")

    return motion


# ---- CLI TESTING ONLY (NOT USED BY GUI) ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m video_module.video_experiments <video.mp4>")
        sys.exit(1)

    process_single_video(sys.argv[1])

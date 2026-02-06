import os

from video_module.videoreader import VideoReader
from video_module.frame_extractor import extract_frames
from video_module.frame_preprocessing import preprocess_frames
from video_module.motion_calculator import calculate_motion_array


def process_single_video(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    extracted_dir = os.path.join("extracted_frames", video_name)
    preprocessed_dir = os.path.join("preprocessed_frames", video_name)

    video = VideoReader(video_path)
    video.open_video()
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


def run_experiments_from_folder():
    folder_path = input("👉 Enter videos folder path: ").strip()

    videos = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".mp4")
    ]

    results = {}

    for video in videos:
        results[os.path.basename(video)] = process_single_video(video)

    print("\n📊 FINAL RESULTS")
    for k, v in results.items():
        print(f"{k} → motion array length: {len(v)}")


if __name__ == "__main__":
    run_experiments_from_folder()
    


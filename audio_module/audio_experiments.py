import sys
import os
import numpy as np
import librosa
import soundfile as sf
from moviepy import VideoFileClip


OUTPUT_FOLDER = "audio_results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def process_single_video(video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    print(f"\n🔊 Processing audio for: {video_name}")

    # -------- Extract Audio --------
    audio_wav = os.path.join(OUTPUT_FOLDER, video_name + "_audio.wav")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_wav, logger=None)

    # -------- Load & Clean Audio --------
    y, sr = librosa.load(audio_wav, sr=16000, mono=True)

    if np.max(np.abs(y)) != 0:
        y = y / np.max(np.abs(y))      # normalize

    y = y - np.mean(y)                 # simple noise reduction

    clean_audio = os.path.join(OUTPUT_FOLDER, video_name + "_clean.wav")
    sf.write(clean_audio, y, sr)

    # -------- Energy Feature --------
    frame_size = 2048
    hop_size = 512

    energy = []
    for i in range(0, len(y) - frame_size, hop_size):
        frame = y[i:i + frame_size]
        e = np.sum(frame ** 2)
        energy.append(e)

    energy = np.array(energy)

    energy_file = os.path.join(OUTPUT_FOLDER, video_name + "_energy.txt")
    np.savetxt(energy_file, energy)

    # -------- Silence Detection --------
    if len(energy) > 0:
        threshold = np.mean(energy) * 0.5
        silence_flags = (energy < threshold).astype(int)
    else:
        silence_flags = []

    silence_file = os.path.join(OUTPUT_FOLDER, video_name + "_silence.txt")
    np.savetxt(silence_file, silence_flags)

    print(f"✅ Audio processing complete for {video_name}")

    return {
        "energy_points": len(energy),
        "silence_points": len(silence_flags)
    }


def run_experiments_from_folder(folder_path):
    videos = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".mp4")
    ]

    if len(videos) == 0:
        raise RuntimeError("No MP4 files found in the given folder")

    results = {}

    for video in videos:
        results[os.path.basename(video)] = process_single_video(video)

    print("\n📊 AUDIO FINAL RESULTS")
    for k, v in results.items():
        print(f"{k} → {v}")

    return results


# -------- ENTRY POINT --------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide a FOLDER path containing videos")
        sys.exit(1)

    folder_path = sys.argv[1]

    try:
        print(f"Running audio pipeline on folder: {folder_path}")
        run_experiments_from_folder(folder_path)
    except Exception as e:
        print("❌ AUDIO PIPELINE FAILED")
        print(e)
        sys.exit(1)

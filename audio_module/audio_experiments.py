import os
import numpy as np
import librosa
import soundfile as sf
from moviepy import VideoFileClip

# -----------------------------
#  FOLDER STRUCTURE YOU SHOULD HAVE
# -----------------------------
# Deepfake_Project/
# ├── videos/            <-- put all your input .mp4 files here
# └── results/           <-- outputs will be stored here (created automatically)
# -----------------------------

INPUT_VIDEO_FOLDER = "videos"
OUTPUT_FOLDER = "results"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_single_video(video_path, video_name):
    """
    This function applies the SAME logic as Files 1–4
    but automatically for one video at a time.
    """

    print(f"\nProcessing: {video_name}")

    # -------- FILE 1: Extract Audio --------
    audio_wav = os.path.join(OUTPUT_FOLDER, video_name + "_audio.wav")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_wav)

    # -------- FILE 2: Preprocess Audio --------
    y, sr = librosa.load(audio_wav, sr=16000, mono=True)
    y = y / np.max(np.abs(y))          # normalize
    y = y - np.mean(y)                 # basic noise reduction

    clean_audio = os.path.join(OUTPUT_FOLDER, video_name + "_clean.wav")
    sf.write(clean_audio, y, sr)

    # -------- FILE 3: Energy Features --------
    frame_size = 2048
    hop_size = 512

    energy = []
    for i in range(0, len(y), hop_size):
        frame = y[i:i+frame_size]
        if len(frame) < frame_size:
            break
        e = np.sum(frame**2)
        energy.append(e)

    energy = np.array(energy)

    energy_file = os.path.join(OUTPUT_FOLDER, video_name + "_energy.txt")
    np.savetxt(energy_file, energy)

    # -------- FILE 4: Silence Detection --------
    threshold = np.mean(energy) * 0.5
    silence_flags = (energy < threshold).astype(int)

    silence_file = os.path.join(OUTPUT_FOLDER, video_name + "_silence.txt")
    np.savetxt(silence_file, silence_flags)

    print(f"Finished: {video_name}")
    print(f"Saved → audio, clean audio, energy, silence flags in {OUTPUT_FOLDER}\n")


# ------------- MAIN BATCH LOOP -------------
if __name__ == "__main__":

    video_files = [f for f in os.listdir(INPUT_VIDEO_FOLDER) if f.endswith(".mp4")]

    if len(video_files) == 0:
        print("No .mp4 files found in 'videos' folder!")
        exit()

    print(f"Found {len(video_files)} videos.\n")

    for video in video_files:
        full_path = os.path.join(INPUT_VIDEO_FOLDER, video)
        name_without_ext = os.path.splitext(video)[0]

        process_single_video(full_path, name_without_ext)

    print("✅ BATCH PROCESSING COMPLETE!")

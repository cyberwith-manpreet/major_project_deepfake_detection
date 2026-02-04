import librosa
import soundfile as sf
import numpy as np

audio_path = "extracted_audio.wav"
clean_path = "clean_audio.wav"

# Load audio in mono
y, sr = librosa.load(audio_path, sr=16000, mono=True)

# Normalize volume
y = y / np.max(np.abs(y))

# Simple noise reduction (mean subtraction)
y = y - np.mean(y)

# Save cleaned audio
sf.write(clean_path, y, sr)

print("Preprocessed audio saved as clean_audio.wav")

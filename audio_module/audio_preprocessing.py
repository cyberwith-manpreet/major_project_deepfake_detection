import librosa
import soundfile as sf
import numpy as np

audio_path = "extracted_audio.wav"
clean_path = "clean_audio.wav"


y, sr = librosa.load(audio_path, sr=16000, mono=True)


y = y / np.max(np.abs(y))


y = y - np.mean(y)


sf.write(clean_path, y, sr)

print("Preprocessed audio saved as clean_audio.wav")

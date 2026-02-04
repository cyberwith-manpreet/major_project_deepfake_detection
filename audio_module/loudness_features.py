import librosa
import numpy as np

audio_path = "clean_audio.wav"

y, sr = librosa.load(audio_path, sr=16000)

frame_size = 2048
hop_size = 512

energy = []

for i in range(0, len(y), hop_size):
    frame = y[i:i+frame_size]
    if len(frame) < frame_size:
        break
    e = np.sum(frame**2)   # Energy calculation
    energy.append(e)

energy = np.array(energy)

np.savetxt("energy_features.txt", energy)

print("Energy features saved!")

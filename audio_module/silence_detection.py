import numpy as np

energy = np.loadtxt("energy_features.txt")

threshold = np.mean(energy) * 0.5

silence = energy < threshold

np.savetxt("silence_flags.txt", silence.astype(int))

print("Silence regions marked!")

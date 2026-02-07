import numpy as np
from logic.mismatch_metrics import absolute_difference

def shift_sequence(seq, shift):
  
    seq = np.array(seq, dtype=float)

    if shift == 0:
        return seq

    shifted = np.zeros_like(seq)

    if shift > 0:
        shifted[shift:] = seq[:-shift]
    else:
        shifted[:shift] = seq[-shift:]

    return shifted


def compute_total_mismatch(audio_seq, video_seq):
    
    diff = absolute_difference(audio_seq, video_seq)
    return np.mean(diff)


def find_best_shift(audio_seq, video_seq, max_shift=10):
 
    audio_seq = np.array(audio_seq, dtype=float)
    video_seq = np.array(video_seq, dtype=float)

    if len(audio_seq) != len(video_seq):
        raise ValueError("Sequences must be aligned first.")

    best_shift = 0
    best_score = float("inf")

    scores = {}

    for shift in range(-max_shift, max_shift + 1):
        shifted_audio = shift_sequence(audio_seq, shift)
        score = compute_total_mismatch(shifted_audio, video_seq)

        scores[shift] = score

        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift, best_score, scores


def tune_threshold(audio_seq, video_seq, max_shift=10):
  
    best_shift, best_score, scores = find_best_shift(
        audio_seq,
        video_seq,
        max_shift
    )

    return {
        "best_shift": best_shift,
        "lowest_mismatch": best_score,
        "all_scores": scores
    }

# Testing the module
if __name__ == "__main__":
    print("Testing threshold tuning...")

    audio = [1, 2, 3, 4, 5, 6]
    video = [0, 1, 2, 3, 4, 5]

    results = tune_threshold(audio, video, max_shift=3)

    print("Best shift:", results["best_shift"])
    print("Lowest mismatch:", results["lowest_mismatch"])

# mismatch_metrics.py


import numpy as np


def validate_inputs(audio_seq, video_seq):
   
    if len(audio_seq) != len(video_seq):
        raise ValueError("Audio and video sequences must be aligned and equal in length.")


def absolute_difference(audio_seq, video_seq):
   
    audio_seq = np.array(audio_seq, dtype=float)
    video_seq = np.array(video_seq, dtype=float)

    validate_inputs(audio_seq, video_seq)

    return np.abs(audio_seq - video_seq)


def squared_difference(audio_seq, video_seq):
    
    audio_seq = np.array(audio_seq, dtype=float)
    video_seq = np.array(video_seq, dtype=float)

    validate_inputs(audio_seq, video_seq)

    return (audio_seq - video_seq) ** 2


def moving_average_difference(audio_seq, video_seq, window_size=5):
  
    abs_diff = absolute_difference(audio_seq, video_seq)

    if window_size <= 1:
        return abs_diff

    kernel = np.ones(window_size) / window_size
    moving_avg = np.convolve(abs_diff, kernel, mode="valid")

    return moving_avg


de
    abs_diff = absolute_difference(audio_seq, video_seq)
    sq_diff = squared_difference(audio_seq, video_seq)
    mov_avg_diff = moving_average_difference(audio_seq, video_seq, window_size)

    return {
        "absolute_difference": abs_diff,
        "squared_difference": sq_diff,
        "moving_average_difference": mov_avg_diff,
    }



if __name__ == "__main__":
    print("Testing mismatch metrics...")

    audio = [1, 2, 3, 4, 5]
    video = [1.1, 1.9, 3.2, 3.8, 4.7]

    results = compute_all_metrics(audio, video)

    print("Absolute difference:", results["absolute_difference"])
    print("Squared difference:", results["squared_difference"])
    print("Moving average difference:", results["moving_average_difference"])

import numpy as np
def trim_to_min_length(audio_seq, video_seq):
  
    min_len = min(len(audio_seq), len(video_seq))

    audio_trimmed = audio_seq[:min_len]
    video_trimmed = video_seq[:min_len]

    return audio_trimmed, video_trimmed


def stretch_sequence(seq, target_length):
  
    if len(seq) == target_length:
        return seq

    original_indices = np.linspace(0, len(seq) - 1, num=len(seq))
    target_indices = np.linspace(0, len(seq) - 1, num=target_length)

    stretched_seq = np.interp(target_indices, original_indices, seq)

    return stretched_seq


def match_lengths_by_stretch(audio_seq, video_seq):

    len_audio = len(audio_seq)
    len_video = len(video_seq)

    if len_audio > len_video:
        video_seq = stretch_sequence(video_seq, len_audio)
    elif len_video > len_audio:
        audio_seq = stretch_sequence(audio_seq, len_video)

    return audio_seq, video_seq


def generate_index_mapping(audio_len, video_len):
  
    audio_indices = np.linspace(0, audio_len - 1, num=max(audio_len, video_len))
    video_indices = np.linspace(0, video_len - 1, num=max(audio_len, video_len))

    return audio_indices.astype(int), video_indices.astype(int)


def align_signals(audio_seq, video_seq, method="stretch"):
  

    audio_seq = np.array(audio_seq, dtype=float)
    video_seq = np.array(video_seq, dtype=float)

    if method == "trim":
        aligned_audio, aligned_video = trim_to_min_length(audio_seq, video_seq)

    elif method == "stretch":
        aligned_audio, aligned_video = match_lengths_by_stretch(audio_seq, video_seq)

    else:
        raise ValueError("Method must be 'trim' or 'stretch'")

    index_map = generate_index_mapping(len(aligned_audio), len(aligned_video))

    return aligned_audio, aligned_video, index_map

# Testing the module
if __name__ == "__main__":
    audio = np.random.rand(120)
    video = np.random.rand(90)

    a, v, idx = align_signals(audio, video, method="stretch")

    print("Aligned audio length:", len(a))
    print("Aligned video length:", len(v))

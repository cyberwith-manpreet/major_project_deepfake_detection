import numpy as np

from logic.align_signals import align_signals
from logic.mismatch_metrics import compute_all_metrics
from logic.threshold_tuning import tune_threshold
from logic.rule_based_classifier import run_classifier

def generate_sample_data():
    """
    Generate simulated audio/video feature sequences.
    """
    np.random.seed(42)

    # Simulated real signal
    base_signal = np.sin(np.linspace(0, 10, 120))

    # Video features (slightly noisy)
    video = base_signal + np.random.normal(0, 0.05, 120)

    # Audio features (shifted + noisy → simulate mismatch)
    audio_full = np.roll(base_signal, 3) + np.random.normal(0, 0.1, 120)
    audio = audio_full[:100]


    return audio, video


def run_pipeline():
    print("\n=== Running Deepfake Detection Pipeline ===\n")

    # Step 1: Sample data
    audio, video = generate_sample_data()
    print("Original lengths -> Audio:", len(audio), "Video:", len(video))

    # Step 2: Align signals
    aligned_audio, aligned_video, _ = align_signals(audio, video)
    print("Aligned length:", len(aligned_audio))

    # Step 3: Compute mismatch metrics
    metrics = compute_all_metrics(aligned_audio, aligned_video)
    avg_mismatch = np.mean(metrics["absolute_difference"])
    print("Average mismatch:", round(avg_mismatch, 4))

    # Step 4: Threshold tuning
    tuning_result = tune_threshold(aligned_audio, aligned_video)
    best_shift = tuning_result["best_shift"]
    lowest_mismatch = tuning_result["lowest_mismatch"]

    print("Best shift:", best_shift)
    print("Lowest mismatch:", round(lowest_mismatch, 4))

    # Step 5: Classification
    classification = run_classifier(lowest_mismatch)

    print("\n=== Final Result ===")
    print("Confidence %:", classification["confidence_percent"])
    print("Classification:", classification["label"])


if __name__ == "__main__":
    run_pipeline()

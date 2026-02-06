import numpy as np

def score_to_confidence(mismatch_score):
    """
    Convert mismatch score to confidence (0 to 1).

    Lower mismatch = higher confidence.
    """
    confidence = 1 / (1 + mismatch_score)
    return confidence


def classify(confidence, decision_threshold=0.6):
    """
    Classify based on confidence.

    Returns: "GOOD" or "BAD"
    """
    if confidence >= decision_threshold:
        return "GOOD"
    return "BAD"


def run_classifier(mismatch_score, decision_threshold=0.6):
    """
    Full pipeline classifier.

    Returns dictionary with:
    - confidence percentage
    - label
    """
    confidence = score_to_confidence(mismatch_score)
    confidence_percent = confidence * 100

    label = classify(confidence, decision_threshold)

    return {
        "mismatch_score": mismatch_score,
        "confidence_percent": round(confidence_percent, 2),
        "label": label
    }

# Testing the module
if __name__ == "__main__":
    print("Testing rule-based classifier...")

    test_score = 0.25

    result = run_classifier(test_score)

    print("Mismatch score:", result["mismatch_score"])
    print("Confidence %:", result["confidence_percent"])
    print("Classification:", result["label"])


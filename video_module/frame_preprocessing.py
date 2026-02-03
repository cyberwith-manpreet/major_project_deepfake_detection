import cv2
import os
import numpy as np


def compute_blur_variance(gray_image):
    """
    Compute Laplacian variance (blur score)
    Higher value = sharper image
    Lower value = blurrier image
    """
    return cv2.Laplacian(gray_image, cv2.CV_64F).var()


def preprocess_frames(
    input_folder="extracted_frames",
    output_folder="preprocessed_frames",
    resize_dim=(224, 224),
    blur_threshold=20.0
):
    """
    Reads extracted frames, resizes them, converts to grayscale,
    computes blur score, and saves all frames.
    """

    # 🔹 Project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_path = os.path.join(project_root, input_folder)
    output_path = os.path.join(project_root, output_folder)

    if not os.path.exists(input_path):
        raise FileNotFoundError("❌ extracted_frames folder not found")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    frame_files = sorted(os.listdir(input_path))

    blur_scores = []
    blurry_count = 0

    print("⏳ Preprocessing frames...")

    for frame_name in frame_files:
        frame_path = os.path.join(input_path, frame_name)

        image = cv2.imread(frame_path)

        if image is None:
            continue

        
        image = cv2.resize(image, resize_dim)

        # 🔹 Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        
        blur_variance = compute_blur_variance(gray)
        blur_scores.append(blur_variance)

        if blur_variance < blur_threshold:
            blurry_count += 1

        
        save_path = os.path.join(output_path, frame_name)
        cv2.imwrite(save_path, gray)

    print("✅ Frame preprocessing completed")
    print(f"📁 Total frames processed: {len(frame_files)}")
    print(f"⚠️ Frames below blur threshold: {blurry_count}")
    print(f"📊 Average blur variance: {np.mean(blur_scores):.2f}")
    print(f"📂 Output folder: {output_path}")

    return np.array(blur_scores)




if __name__ == "__main__":
    try:
        blur_array = preprocess_frames()
        print("\nBlur Variance Array:")
        print(blur_array)
    except Exception as e:
        print("❌ Error:", e)

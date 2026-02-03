import cv2
import os


def is_blurry(image, threshold=100.0):
    """
    Check if image is blurry using Laplacian Variance
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold


def preprocess_frames(
    input_folder="extracted_frames",
    output_folder="preprocessed_frames",
    resize_dim=(224, 224)
):
    """
    Read all frames, resize, convert to grayscale,
    remove blurry frames, and save clean frames
    """

    # 🔹 Project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_path = os.path.join(project_root, input_folder)
    output_path = os.path.join(project_root, output_folder)

    if not os.path.exists(input_path):
        raise FileNotFoundError("❌ Extracted frames folder not found")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    frame_files = sorted(os.listdir(input_path))

    processed_count = 0
    skipped_blur = 0

    print("⏳ Preprocessing frames...")

    for frame_name in frame_files:
        frame_path = os.path.join(input_path, frame_name)

        image = cv2.imread(frame_path)

        if image is None:
            continue

        # 🔹 Blur check
        if is_blurry(image):
            skipped_blur += 1
            continue

        # 🔹 Resize
        image = cv2.resize(image, resize_dim)

        # 🔹 Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        save_path = os.path.join(output_path, frame_name)
        cv2.imwrite(save_path, gray)

        processed_count += 1

    print("✅ Frame preprocessing completed")
    print(f"✔ Frames processed & saved: {processed_count}")
    print(f"✖ Blurry frames removed: {skipped_blur}")
    print(f"📁 Output folder: {output_path}")




if __name__ == "__main__":
    try:
        preprocess_frames()
    except Exception as e:
        print("❌ Error:", e)

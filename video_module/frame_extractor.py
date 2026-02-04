import cv2
import os


def extract_frames(video_path, output_folder):
    # Validate MP4
    if not video_path.lower().endswith(".mp4"):
        raise ValueError("Only MP4 videos are supported")

    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    print("⏳ Extracting frames...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_name = f"frame_{frame_count:04d}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ Total Frames Extracted: {frame_count}")
    print(f"📁 Frames saved in folder: {output_folder}")

    return frame_count


if __name__ == "__main__":
    video_path = input("👉 Enter MP4 video path: ").strip()
    output_folder = "extracted_frames"

    try:
        extract_frames(video_path, output_folder)
        print("✅ Frame extraction completed successfully")
    except Exception as e:
        print("❌ Error:", e)

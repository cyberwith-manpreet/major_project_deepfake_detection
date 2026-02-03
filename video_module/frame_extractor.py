import cv2
import os

def extract_frames(video_path, output_folder="extracted_frames"):
    """
    Extract all frames from MP4 video and save them into a folder
    """

    
    if not video_path.lower().endswith(".mp4"):
        raise ValueError("Only MP4 videos are supported")

    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, output_folder)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Error opening video file")

    frame_count = 0

    print("⏳ Extracting frames...")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_filename = f"frame_{frame_count:04d}.jpg"
        frame_filepath = os.path.join(output_path, frame_filename)

        cv2.imwrite(frame_filepath, frame)
        frame_count += 1

    cap.release()

    print(f"✅ Total Frames Extracted: {frame_count}")
    print(f"📁 Frames saved in folder: {output_path}")

    return frame_count



if __name__ == "__main__":
    video_path = input("👉 Enter MP4 video path: ").strip()

    try:
        total = extract_frames(video_path)
        print("✅ Frame extraction completed successfully")

    except Exception as e:
        print("❌ Error:", e)


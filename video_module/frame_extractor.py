import cv2
import os

def extract_frames(video_path, output_folder):
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
        cv2.imwrite(os.path.join(output_folder, frame_name), frame)
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ Total Frames Extracted: {frame_count}")

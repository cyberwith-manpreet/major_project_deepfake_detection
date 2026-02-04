import cv2
import os
import numpy as np

def preprocess_frames(input_folder, output_folder, size=(128,128)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frames = sorted(os.listdir(input_folder))
    blur_values = []

    print("⏳ Preprocessing frames...")

    for frame_name in frames:
        frame_path = os.path.join(input_folder, frame_name)
        frame = cv2.imread(frame_path)

        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, size)

        blur_var = cv2.Laplacian(resized, cv2.CV_64F).var()
        blur_values.append(blur_var)

        cv2.imwrite(os.path.join(output_folder, frame_name), resized)

    print("✅ Frame preprocessing completed")
    print(f"📁 Total frames processed: {len(blur_values)}")
    print(f"📊 Average blur variance: {np.mean(blur_values):.2f}")

    return blur_values

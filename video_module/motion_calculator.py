import cv2
import os
import numpy as np


def calculate_motion_array(input_folder="preprocessed_frames"):
    """
    Reads consecutive frames, subtracts pixel values,
    and returns an array of motion (frame difference values)
    """

    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(project_root, input_folder)

    if not os.path.exists(input_path):
        raise FileNotFoundError("❌ Preprocessed frames folder not found")

    frame_files = sorted(os.listdir(input_path))

    if len(frame_files) < 2:
        raise ValueError("❌ Not enough frames to calculate motion")

    motion_array = []

    print("⏳ Calculating temporal motion differences...")

    for i in range(len(frame_files) - 1):
        frame1_path = os.path.join(input_path, frame_files[i])
        frame2_path = os.path.join(input_path, frame_files[i + 1])

        frame1 = cv2.imread(frame1_path, cv2.IMREAD_GRAYSCALE)
        frame2 = cv2.imread(frame2_path, cv2.IMREAD_GRAYSCALE)

        if frame1 is None or frame2 is None:
            continue

        
        diff = cv2.absdiff(frame1, frame2)

        
        diff_value = np.sum(diff)

        motion_array.append(diff_value)

    print("✅ Motion calculation completed")
    print(f"📊 Motion array length: {len(motion_array)}")

    return np.array(motion_array)




if __name__ == "__main__":
    try:
        motion = calculate_motion_array()
        print("\nMotion Difference Array:")
        print(motion)

    except Exception as e:
        print("❌ Error:", e)


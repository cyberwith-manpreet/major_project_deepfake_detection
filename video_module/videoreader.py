import cv2
import os

class VideoReader:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = None

    def is_mp4(self):
        return self.video_path.lower().endswith(".mp4")

    def open_video(self):
        if not os.path.exists(self.video_path):
            raise FileNotFoundError("❌ Video file not found")

        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            raise ValueError("❌ Error opening video file")

    def get_video_properties(self):
        if self.cap is None:
            raise Exception("❌ Video not opened")

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps != 0 else 0

        # ✅ DICTIONARY RETURN (IMPORTANT FIX)
        return {
            "fps": fps,
            "total_frames": total_frames,
            "duration_seconds": duration
        }

    def release(self):
        if self.cap:
            self.cap.release()

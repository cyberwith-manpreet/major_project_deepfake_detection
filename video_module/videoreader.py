import cv2
import os


class VideoReader:
    def __init__(self, video_path):
        self.video_path = os.path.abspath(video_path)
        self.cap = None

    def open_video(self):
        if not os.path.isfile(self.video_path):
            print("❌ File does not exist:", self.video_path)
            return False

        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            print("❌ OpenCV cannot open video:", self.video_path)
            return False

        return True

    def get_video_properties(self):
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        duration_seconds = total_frames / fps if fps > 0 else 0

        return {
            "total_frames": total_frames,
            "fps": fps,
            "duration_seconds": duration_seconds
        }

    def release(self):
        if self.cap:
            self.cap.release()

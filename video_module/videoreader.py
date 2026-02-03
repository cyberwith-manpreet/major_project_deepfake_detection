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

        return fps, total_frames, duration

    def release(self):
        if self.cap:
            self.cap.release()

if __name__ == "__main__":

    video_path = input("👉 Enter the video path: ").strip()

    video = VideoReader(video_path)

    # MP4 check
    if not video.is_mp4():
        print("❌ Please enter video path of only MP4 videos")
        exit()

    print("✅ MP4 format verified")
    print("⏳ Analyzing video...")

    try:
        video.open_video()
        print("✅ Video read successfully")

        fps, total_frames, duration = video.get_video_properties()

        print("\n📊 Video Analysis Result:")
        print(f"• Video FPS (Speed): {fps:.2f}")
        print(f"• Total Frames (Images): {total_frames}")
        print(f"• Video Duration: {duration:.2f} seconds")

        print("\n✅ Video read and analyzed successfully")

    except Exception as e:
        print(e)

    finally:
        video.release()

from moviepy import VideoFileClip

video_path = "input_video.mp4"
audio_path = "extracted_audio.wav"

video = VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

print("Audio extracted and saved as extracted_audio.wav")

import cv2
import os

def extract_frames(video_path, output_dir, interval_seconds=60):
    """
    Extracts one frame every `interval_seconds` from the video.

    Args:
        video_path (str): Path to the input video.
        output_dir (str): Directory to save extracted frames.
        interval_seconds (int): Seconds between each saved frame.
    """
    os.makedirs(output_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)

    count = 0
    frame_id = 0

    while vidcap.isOpened():
        ret, frame = vidcap.read()
        if not ret:
            break

        if count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{frame_id:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_id += 1

        count += 1

    vidcap.release()

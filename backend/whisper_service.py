import whisper
import os

# Load the model once at module level
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large

def transcribe_audio(file_path):
    """
    Transcribe audio/video using Whisper

    Args:
        file_path (str): Path to the input video or audio file

    Returns:
        str: Transcribed text
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"[INFO] Transcribing: {file_path}")
    result = model.transcribe(file_path)
    return result["text"]

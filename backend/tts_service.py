def text_to_speech(text, output_path="tts_output.wav"):
    # Dummy audio file generator
    with open(output_path, "w") as f:
        f.write("This is simulated speech for: " + text)
    return output_path

import os
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech(text, lang="hi"):
    output_dir = os.path.join("data", "audio")
    os.makedirs(output_dir, exist_ok=True)

    mp3_output_path = os.path.join(output_dir, f"tts_output_{lang}.mp3")
    wav_output_path = mp3_output_path.replace(".mp3", ".wav")

    tts = gTTS(text=text, lang=lang)
    tts.save(mp3_output_path)

    convert_to_wav(mp3_output_path, wav_output_path)

    return {
        "mp3_path": mp3_output_path,
        "wav_path": wav_output_path
    }

def convert_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

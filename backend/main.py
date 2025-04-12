from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS

# Import your services
from whisper_service import transcribe_audio
from ocr_service import extract_text_from_image
from llama_summarizer import summarize_text
from translator_google import translate_text
from tts_service import text_to_speech

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "AI Lecture Capture System API is running."

@app.route("/audio/<filename>")
def get_audio_file(filename):
    audio_path = os.path.join(os.getcwd(), filename)
    if not os.path.exists(audio_path):
        return jsonify({"error": "Audio file not found"}), 404
    return send_file(audio_path, mimetype="audio/wav")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({
        "message": "File uploaded successfully",
        "filename": file.filename
    }), 200

@app.route("/process", methods=["GET"])
def process_all():
    filename = request.args.get("filename")
    target_lang = request.args.get("lang", "hi")  # Default to Hindi

    if not filename:
        return jsonify({"error": "Filename not provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        # Step 1: Transcription
        transcript = transcribe_audio(file_path)

        # Step 2: Summarization
        summary = summarize_text(transcript)

        # Step 3: Translation of full transcription
        translated_transcription = translate_text(transcript, target_lang)

        # Step 4: Text-to-Speech
        audio_path = text_to_speech(translated_transcription, lang=target_lang)

        # Step 5: OCR
        ocr_results = []
        video_id = os.path.splitext(filename)[0]
        frame_dir = os.path.join("data", "frames", video_id)
        ocr_output_dir = os.path.join("data", "ocr_outputs", video_id)
        os.makedirs(ocr_output_dir, exist_ok=True)

        if os.path.exists(frame_dir):
            for img_file in sorted(os.listdir(frame_dir)):
                if img_file.lower().endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(frame_dir, img_file)
                    extracted_text = extract_text_from_image(img_path)
                    
                    # Save OCR result
                    ocr_txt_path = os.path.join(ocr_output_dir, f"{os.path.splitext(img_file)[0]}.txt")
                    with open(ocr_txt_path, "w", encoding="utf-8") as f:
                        f.write(extracted_text)

                    ocr_results.append({
                        "image": img_file,
                        "extracted_text": extracted_text
                    })

        # Final JSON response
        return jsonify({
            "transcription": transcript,
            "summary": summary,
            "translated_transcription": translated_transcription,
            "tts_audio_file": audio_path,
            "ocr": ocr_results
        })

    except Exception as e:
        print(f"[ERROR] Full pipeline failed: {e}")
        return jsonify({"error": "Full pipeline processing failed"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)

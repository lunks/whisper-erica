#!/usr/bin/env python

from flask import Flask, request, jsonify
import tempfile
from faster_whisper import WhisperModel

# Initialize the Flask application
app = Flask(__name__)

# Initialize the Whisper model
model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float32")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Check if a WAV file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    # Check if the uploaded file is a valid WAV file
    if file.filename == '' or not file.filename.endswith('.wav'):
        return jsonify({"error": "No valid WAV file uploaded"}), 400
    
    # Create a temporary WAV file to store the input audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as wav_file:
        # Save the uploaded WAV file to the temporary file
        file.save(wav_file.name)

        # Transcribe the audio
        segments, info = model.transcribe(wav_file.name, beam_size=5, language="pt")

        # Concatenate all text from segments
        full_transcription = " ".join(segment.text for segment in segments)

        return jsonify({"transcription": full_transcription})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

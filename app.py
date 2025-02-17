import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import Transcription_
import Legenda

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp')  # Use /tmp como fallback
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', '/tmp')  # Use /tmp como fallback
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Certifique-se de que os diretórios existem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    output_video = os.path.join(app.config['OUTPUT_FOLDER'], f"output_{filename}")

    try:
        transcricao, transcription_text = Transcription_.print_audio_info_and_transcribe(video_path)
        transcricao = [(word, str(time)) for word, time in transcricao]
        Legenda.process_video(transcricao, video_path, output_video)
        return send_file(output_video, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
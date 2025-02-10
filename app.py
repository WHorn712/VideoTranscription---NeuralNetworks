from flask import Flask, request, jsonify, send_file
import os
import Transcription_
import Legenda
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/path/to/upload')  # Use variáveis de ambiente
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', '/path/to/output')  # Use variáveis de ambiente
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Certifique-se de que os diretórios existem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    # Verifica se o arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    # Salva o arquivo de vídeo
    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    # Define o caminho para o vídeo de saída
    output_video = os.path.join(app.config['OUTPUT_FOLDER'], f"output_{filename}")

    # Executa a transcrição e a adição de legendas
    transcricao, transcription_text = Transcription_.print_audio_info_and_transcribe(video_path)
    transcricao = [(word, str(time)) for word, time in transcricao]
    Legenda.process_video(transcricao, video_path, output_video)

    # Retorna o vídeo resultante
    return send_file(output_video, as_attachment=True)


@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200
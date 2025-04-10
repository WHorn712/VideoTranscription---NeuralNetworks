import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import Transcription_
import Legenda
import requests
import time

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', '/tmp')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Certifique-se de que os diretórios existem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Chave secreta para webhook
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    # Obtenha os parâmetros video_id e webhook_url do corpo da requisição
    video_id = request.form.get('video_id')
    webhook_url = request.form.get('webhook_url')
    output_filename = f"output_{video_id}.mp4"
    output_video = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        transcricao, transcription_text = Transcription_.print_audio_info_and_transcribe(video_path)
        transcricao = [(word, str(time)) for word, time in transcricao]
        Legenda.process_video(transcricao, video_path, output_video)

        # Envie a notificação para o webhook
        headers = {'X-Webhook-Token': WEBHOOK_SECRET}
        # Monta a URL do vídeo para o subdomínio videos.legendasoficial.com
        video_url = f"https://videos.legendasoficial.com/{output_filename}"
        data = {'video_id': video_id, 'video_url': video_url}
        response = requests.post(webhook_url, headers=headers, json=data)

        if response.status_code != 200:
            print(f"Erro ao enviar notificação para o webhook: {response.status_code}")
            # Lide com o erro aqui (por exemplo, tente novamente mais tarde)
        return jsonify({"message": "Vídeo transcrito com sucesso."}), 200

    except Exception as e:
        print(f"Erro no processamento da transcrição: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)

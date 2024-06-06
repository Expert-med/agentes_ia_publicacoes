from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import requests
from firebase_admin import credentials, storage
from datetime import datetime,timedelta  
import firebase_admin

# Inicializar Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'projeto-processos.appspot.com'
})

os.environ['OPENAI_API_KEY'] = "sk-proj-Jx4cJCCUfnxdNm32jx3fT3BlbkFJjsv8CiBVIuXLa5RmxSO1"
openai.api_key = os.environ['OPENAI_API_KEY']

# Inicialização do aplicativo Flask
app = Flask(__name__)
CORS(app)

def baixar_imagem(url, caminho_do_arquivo):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        with open(caminho_do_arquivo, 'wb') as file:
            file.write(response.content)
        
        print(f'Imagem salva com sucesso em {caminho_do_arquivo}')
    
    except requests.exceptions.RequestException as e:
        print(f'Erro ao baixar a imagem: {e}')

def upload_para_firebase(caminho_do_arquivo, nome_do_arquivo):
    bucket = storage.bucket()
    blob = bucket.blob(f'publicacoes/{nome_do_arquivo}')
    blob.upload_from_filename(caminho_do_arquivo)
    print(f'Arquivo {nome_do_arquivo} enviado para o Firebase Storage na pasta publicacao.')
    # Obter a URL da imagem no Firebase Storage
    image_url_firebase = blob.generate_signed_url(datetime.now() + timedelta(days=1), method='GET')

    return image_url_firebase

@app.route('/generate-image-url', methods=['POST'])
def generate_image_url():
    image_desc = request.json.get('image_desc')

    # Verificar se a descrição da imagem foi fornecida
    if not image_desc:
        return jsonify({'error': 'Descrição da imagem ausente'}), 400

    try:
        # Gerar a imagem usando a API OpenAI
        response = openai.Image.create(
            prompt=image_desc,
            n=1,
            size="1024x1024"
        )

        # Obter a URL da imagem gerada
        image_url = response['data'][0]['url']

        # Baixar a imagem
        caminho_para_salvar = 'imagem_baixada.jpg'
        baixar_imagem(image_url, caminho_para_salvar)

        # Gerar o nome do arquivo baseado na data e hora atual
        nome_do_arquivo = datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg'

        # Fazer upload para o Firebase Storage
        image_url_firebase = upload_para_firebase(caminho_para_salvar, nome_do_arquivo)

        # Remover o arquivo local após o upload (opcional)
        os.remove(caminho_para_salvar)

        return jsonify({'image_url': image_url, 'firebase_image_url': image_url_firebase, 'firebase_file_name': nome_do_arquivo})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Set limit to 32MB (or adjust as needed)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8083)))

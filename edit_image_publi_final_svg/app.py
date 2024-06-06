from flask import Flask, request, jsonify
from lxml import etree as ET
from firebase_admin import credentials, storage
import firebase_admin
from datetime import datetime, timedelta  
import os
from flask_cors import CORS
import cairosvg

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'projeto-processos.appspot.com'
})

def convert_svg_to_png(svg_file_path, png_file_path):
    # Use cairosvg para converter o SVG para PNG
    cairosvg.svg2png(url=svg_file_path, write_to=png_file_path)


# Função para salvar a imagem no Firebase
def save_jpeg_to_firebase(local_jpeg_path, firebase_jpeg_name):
    bucket = storage.bucket()
    blob = bucket.blob(f'postagem_final/{firebase_jpeg_name}')
    blob.upload_from_filename(local_jpeg_path)
    jpeg_url_firebase = blob.generate_signed_url(datetime.now() + timedelta(days=1), method='GET')

    return jpeg_url_firebase

# Função para quebrar o texto em várias linhas se ultrapassar as margens
def wrap_text(text, width):
    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line + ' ' + word) <= width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines

@app.route('/generate_svg_and_save_jpeg', methods=['POST'])
def generate_svg_and_save_jpeg():
    # Receber a URL da imagem e o título
    image_url = request.json.get('image_url')
    title = request.json.get('title')

    # Verificar se a URL da imagem e o título foram fornecidos
    if not image_url or not title:
        return {'error': 'URL da imagem ou título ausentes'}, 400

    # Carregar o arquivo SVG existente
    tree = ET.parse('postagem1.svg')
    root = tree.getroot()

    # Coordenadas do retângulo especificado pelo atributo 'd' do elemento <path>
    x1 = 138.320312
    y1 = 241.988281
    x2 = 658.714844
    y2 = 573.386719

    # Calculando a largura e a altura do retângulo
    width = x2 - x1
    height = y2 - y1

    # Criar um novo elemento de imagem
    image = ET.Element('{http://www.w3.org/2000/svg}image', {
        'x': str(x1),
        'y': str(y1),
        'width': str(width),
        'height': str(height),
        '{http://www.w3.org/1999/xlink}href': image_url
    })

    # Adicionar a imagem como um elemento filho do root do SVG
    root.append(image)

    # Definir a posição vertical do texto (um pouco acima do topo)
    text_y = y1 + -125  # Ajuste para cima

    # Adicionar texto no topo do SVG
    text = ET.Element('{http://www.w3.org/2000/svg}text', {
        'x': str(x1 + (width / 2)),  # Centralizando o texto no eixo x
        'y': str(text_y),  # Posição vertical ajustada
        'fill': 'black',  # Cor do texto
        'font-size': '20',  # Tamanho da fonte
        'font-family': 'Arial',
        'font-weight': 'bold',
        'text-anchor': 'middle',  # Centralizando o texto horizontalmente
        'dominant-baseline': 'middle'  # Centralizando o texto verticalmente
    })

    # Adicionando espaçamento ao redor do texto
    text_margin = 25
    text_x = x1 + (width / 2)
    text_y = text_y + text_margin

    # Largura máxima do texto antes de quebrar linha
    max_text_width = width - 2 * text_margin

    # Texto a ser adicionado
    original_text = title

    # Quebrar o texto em várias linhas se ultrapassar as margens
    wrapped_lines = wrap_text(original_text, max_text_width)

    # Adicionar o texto ao SVG, linha por linha
    for index, line in enumerate(wrapped_lines):
        line_y = text_y + index * 25  # Espaçamento de 25px entre as linhas
        line_element = ET.Element('{http://www.w3.org/2000/svg}tspan', {'x': str(text_x), 'dy': '1em'})
        line_element.text = line
        text.append(line_element)

    # Adicionar o texto como um elemento filho do root do SVG
    root.append(text)

    output_png_file = f'saida_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'

# Converter o SVG para PNG
    convert_svg_to_png(output_svg_file, output_png_file)

    # Salvar a imagem PNG no Firebase
    png_url_firebase = save_png_to_firebase(output_png_file, output_png_file)


    # Excluir os arquivos SVG e JPEG locais após o upload
    os.remove(output_svg_file)
    os.remove(output_jpeg_file)

    return {'nome_arquivo_firebase': output_jpeg_file, 'firebase_image_url': jpeg_url_firebase}

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Set limit to 32MB (or adjust as needed)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8083)))
from instabot import Bot
import requests
import os

# URL da imagem que você deseja baixar temporariamente
img_url = "https://e1.pngegg.com/pngimages/167/1012/png-clipart-cute-animals-ii-gray-and-white-kittens-thumbnail.png"

# Nome do arquivo temporário para salvar a imagem
temp_img_path = "temp_image.png"

# Baixar a imagem da URL
response = requests.get(img_url)

# Verificar se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Salvar a imagem no arquivo temporário
    with open(temp_img_path, 'wb') as f:
        f.write(response.content)
    print("Imagem salva temporariamente com sucesso:", temp_img_path)
else:
    print("Falha ao baixar a imagem.")

bot = Bot()

bot.login(username="expertvision.tech", password="c2sbexpertmed")

bot.upload_photo(temp_img_path, caption="titulooooo ")
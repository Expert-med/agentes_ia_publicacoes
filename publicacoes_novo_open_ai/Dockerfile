# Use a imagem oficial do Python 3.11.3 como base
FROM python:3.11.3-slim

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY . .

# Instale as dependências do Flask a partir do requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Defina as variáveis de ambiente necessárias
ENV OPENAI_MODEL_NAME 'gpt-3.5-turbo'
ENV OPENAI_API_KEY 'sk-proj-Jx4cJCCUfnxdNm32jx3fT3BlbkFJjsv8CiBVIuXLa5RmxSO1'
ENV SERPER_API_KEY '0de6e185f983b1d170902c2030540ff023d3904a'

# Exponha a porta 5000 para acessar a aplicação Flask
EXPOSE 8083

# Comando para iniciar a aplicação Flask quando o contêiner for iniciado
CMD ["python", "app.py"]

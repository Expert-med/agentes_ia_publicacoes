# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do aplicativo para o diretório de trabalho
COPY . .

# Defina as variáveis de ambiente necessárias
ENV OPENAI_MODEL_NAME=gpt-3.5-turbo
ENV OPENAI_API_KEY=sk-proj-Jx4cJCCUfnxdNm32jx3fT3BlbkFJjsv8CiBVIuXLa5RmxSO1
ENV SERPER_API_KEY=0de6e185f983b1d170902c2030540ff023d3904a

EXPOSE 8083

# Comando para executar o aplicativo
CMD ["python", "app.py"]

# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Instale as dependências do sistema necessárias para o cairosvg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcairo2-dev \
    libglib2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do aplicativo para o diretório de trabalho
COPY . .

EXPOSE 8083

# Comando para executar o aplicativo
CMD ["python", "app.py"]

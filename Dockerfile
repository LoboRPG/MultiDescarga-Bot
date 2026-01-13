FROM python:3.10-slim

# Instalamos ffmpeg para la música
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Ejecutamos el bot
CMD ["python", "main.py"]

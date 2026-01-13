# Usamos una imagen de Python
FROM python:3.10-slim

# Instalamos FFmpeg (esto es lo que te falta en Koyeb)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copiamos los archivos al servidor
WORKDIR /app
COPY . .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para arrancar tu bot (cambia bot.py por el nombre de tu archivo)
CMD ["python", "bot.py"]

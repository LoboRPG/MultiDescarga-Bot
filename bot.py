import telebot
from telebot import types
import os
import time
import subprocess
import shutil

# CONFIGURACIÓN DEL TOKEN
TOKEN = '8134514604:AAEyYM2bFT7PWIGuCs47bNNODto5tJYzQ6I'
bot = telebot.TeleBot(TOKEN)

# Directorio temporal para descargas y portadas
TEMP_DIR = "descargas_bot"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def limpieza_automatica():
    """Borra archivos descargados y miniaturas para que Koyeb no se llene"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
    # Limpia el caché de yt-dlp para ahorrar espacio en disco
    subprocess.run(["yt-dlp", "--clear-cache"], stdout=subprocess.DEVNULL)
    print("🧹 Memoria de Koyeb liberada y archivos borrados.")

# COMANDO /START
@bot.message_handler(commands=['start', 'Star'])
def send_welcome(message):
    limpieza_automatica()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Música 🎵')
    item2 = types.KeyboardButton('Video 🎥')
    item3 = types.KeyboardButton('Limpiar Memoria 🧹')
    markup.add(item1, item2, item3)
    bot.reply_to(message, "🚀 Bot de Descargas Activo.\nEnvía un nombre o link para empezar.", reply_markup=markup)

# MANEJADOR DE MENÚ
@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.text == 'Música 🎵':
        msg = bot.send_message(message.chat.id, "🎵 Escribe el nombre de la canción o el link:")
        bot.register_next_step_handler(msg, download_audio)
    elif message.text == 'Video 🎥':
        msg = bot.send_message(message.chat.id, "🎥 Escribe el nombre del video o el link:")
        bot.register_next_step_handler(msg, download_video)
    elif message.text == 'Limpiar Memoria 🧹':
        limpieza_automatica()
        bot.send_message(message.chat.id, "✅ Se han borrado todos los archivos temporales de la nube.")

# FUNCIÓN: DESCARGAR MÚSICA CON PORTADA
def download_audio(message):
    query = message.text
    bot.send_message(message.chat.id, "📥 Buscando y procesando música con portada...")
    
    # Configuración de salida: guarda audio y miniatura
    output_template = os.path.join(TEMP_DIR, "%(title)s.%(ext)s")
    
    # Comando yt-dlp: Extrae audio, convierte a mp3 y descarga la miniatura (portada)
    cmd = [
        "yt-dlp", 
        "-f", "bestaudio", 
        "--extract-audio", 
        "--audio-format", "mp3", 
        "--write-thumbnail", 
        "--convert-thumbnails", "jpg",
        "-o", output_template, 
        f"ytsearch1:{query}"
    ]
    
    subprocess.run(cmd)
    
    try:
        # Buscar el archivo mp3 y la imagen en el directorio
        archivos = os.listdir(TEMP_DIR)
        mp3_file = next(f for f in archivos if f.endswith(".mp3"))
        thumb_file = next((f for f in archivos if f.endswith(".jpg") or f.endswith(".webp")), None)
        
        path_audio = os.path.join(TEMP_DIR, mp3_file)
        
        if thumb_file:
            path_thumb = os.path.join(TEMP_DIR, thumb_file)
            with open(path_audio, 'rb') as audio, open(path_thumb, 'rb') as thumb:
                bot.send_audio(message.chat.id, audio, thumb=thumb, caption=f"✅ {mp3_file}")
        else:
            with open(path_audio, 'rb') as audio:
                bot.send_audio(message.chat.id, audio, caption=f"✅ {mp3_file}")
        
        # BORRADO AUTOMÁTICO después de enviar
        limpieza_automatica()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: No se pudo procesar la música.")
        limpieza_automatica()

# FUNCIÓN: DESCARGAR VIDEO
def download_video(message):
    query = message.text
    bot.send_message(message.chat.id, "📥 Descargando video...")
    output_template = os.path.join(TEMP_DIR, "video.%(ext)s")
    
    subprocess.run(["yt-dlp", "-f", "best[ext=mp4]", "-o", output_template, f"ytsearch1:{query}"])
    
    try:
        archivo_video = os.path.join(TEMP_DIR, "video.mp4")
        with open(archivo_video, 'rb') as v:
            bot.send_video(message.chat.id, v)
        limpieza_automatica()
    except:
        bot.send_message(message.chat.id, "❌ Error al descargar video.")
        limpieza_automatica()

# INICIO DEL BOT CON RECONEXIÓN
if __name__ == '__main__':
    print("🚀 Bot de música iniciado en Koyeb...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception:
            time.sleep(5)

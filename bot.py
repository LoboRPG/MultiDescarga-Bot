import telebot
import yt_dlp
import os
import subprocess

# TU NUEVO TOKEN ACTUALIZADO
TOKEN = '7774776104:AAEqfG_26rW6YlJp-K8u5X23qNf-j-6vcU'
bot = telebot.TeleBot(TOKEN)

# Carpeta temporal de descargas
DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Envíame el nombre de una canción y te la enviaré en versión Lyrics con su portada.")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text
    # Forzamos la búsqueda de la versión Lyrics
    search_query = f"ytsearch1:{query} lyrics"
    
    msg = bot.reply_to(message, f"🔍 Buscando '{query}' en versión Lyrics...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }, {
            'key': 'EmbedThumbnail',
        }],
        'writethumbnail': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            video_title = info['entries'][0]['title']
            file_path = f"{DOWNLOAD_DIR}/{video_title}.mp3"

        # Enviamos el archivo con la portada
        with open(file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=video_title)
        
        # LIMPIEZA DE MEMORIA: Borramos el archivo para no llenar el disco de Koyeb
        os.remove(file_path)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, msg.message_id)

# ESTA LÍNEA ES VITAL PARA QUE KOYEB NO CIERRE EL BOT (EVITA EL ERROR 0)
print("Bot encendido correctamente...")
bot.polling(none_stop=True)

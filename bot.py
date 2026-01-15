import telebot
import yt_dlp
import os
import shutil

# NUEVO TOKEN (Cambiado para evitar conflictos)
TOKEN = '8134514604:AAHatZbJL4PUiii9fZZKuTySdFGH-E-6vcU'
bot = telebot.TeleBot(TOKEN)

# Carpeta de trabajo (Se limpia automáticamente)
TEMP_DIR = "downloads"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎵 ¡Bot de Música Lyrics Activo!\nEnvíame el nombre de una canción y te la enviaré con portada.")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text
    chat_id = message.chat.id
    
    # Agregamos "lyrics" para audio limpio de ruidos de video
    search_query = f"{query} lyrics"
    msg = bot.send_message(chat_id, f"🔍 Procesando versión Lyrics: {query}...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
        'writethumbnail': True, # Descarga la imagen
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {'key': 'EmbedThumbnail'}, # Pega la foto al audio
            {'key': 'FFmpegMetadata'},
        ],
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Busca y descarga usando yt-dlp y ffmpeg
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            # Ajuste de nombre de archivo para MP3
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
            if os.path.exists(filename):
                with open(filename, 'rb') as audio:
                    bot.send_audio(chat_id, audio, title=info.get('title'), performer=info.get('uploader'))
                bot.delete_message(chat_id, msg.message_id)
            else:
                bot.edit_message_text("❌ Error: No se pudo generar el archivo MP3.", chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text

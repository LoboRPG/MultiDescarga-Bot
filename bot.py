import telebot
import yt_dlp
import os
import shutil

# Token de tu bot
TOKEN = '8134514604:AAEyYM2bFT7PWIGuCs47bNNODto5tJYzQ6I'
bot = telebot.TeleBot(TOKEN)

# Carpeta de descargas
TEMP_DIR = "downloads"

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎵 ¡Bot de Música Lyrics Activo! Envíame el nombre de una canción.")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text
    chat_id = message.chat.id
    
    # Agregamos "lyrics" a la búsqueda para evitar videos oficiales con ruidos
    search_query = f"{query} lyrics"
    msg = bot.send_message(chat_id, f"🔍 Buscando versión Lyrics para: {query}...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
        'writethumbnail': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ],
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Busca y descarga la versión lyrics
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3').replace('.mkv', '.mp3')
            
            with open(filename, 'rb') as audio:
                bot.send_audio(chat_id, audio, title=info.get('title'), performer=info.get('uploader'))
            
            bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error Técnico: {str(e)}\n\n(Asegúrate de tener el archivo Aptfile con la palabra ffmpeg en GitHub)", chat_id, msg.message_id)
    
    finally:
        # Limpieza automática para que Koyeb no falle por espacio
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            os.makedirs(TEMP_DIR)

print("🚀 Bot optimizado para Lyrics iniciado...")
bot.polling()

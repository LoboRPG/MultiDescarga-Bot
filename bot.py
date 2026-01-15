import telebot
import yt_dlp
import os

TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

# Carpeta de descargas
DL_DIR = 'downloads'
if not os.path.exists(DL_DIR):
    os.makedirs(DL_DIR)

@bot.message_handler(func=lambda m: True)
def download(message):
    query = message.text
    msg = bot.reply_to(message, f"🎵 Buscando: {query}...")
    
    # Opciones ultra-compatibles
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DL_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'default_search': 'ytsearch',
        # Forzamos a no usar cookies y usar un agente simple
        'nocheckcertificate': True,
        'quiet': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Buscamos directamente el término con 'lyrics'
            info = ydl.extract_info(f"{query} lyrics", download=True)
            title = info['entries'][0]['title']
            path = f"{DL_DIR}/{title}.mp3"

        with open(path, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=title)
        
        os.remove(path)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Reintenta con: {query}", message.chat.id, msg.message_id)

print("Bot listo en modo simple...")
bot.polling(none_stop=True)

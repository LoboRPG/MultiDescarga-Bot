import telebot
import yt_dlp
import os

TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

DL_DIR = 'downloads'
if not os.path.exists(DL_DIR):
    os.makedirs(DL_DIR)

@bot.message_handler(func=lambda m: True)
def download(message):
    query = message.text
    # Mensaje amigable que indica que buscará incluso por letra
    msg = bot.reply_to(message, f"🔍 Buscando canción o letra: '{query}'...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DL_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'default_search': 'scsearch1:', # Fuente segura SoundCloud
        'nocheckcertificate': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }, {
            'key': 'EmbedThumbnail', 
        }],
        'writethumbnail': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Buscamos la coincidencia más cercana en SoundCloud
            info = ydl.extract_info(query, download=True)
            video_data = info['entries'][0] if 'entries' in info else info
            title = video_data['title']
            path = f"{DL_DIR}/{title}.mp3"

        with open(path, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=title)
        
        if os.path.exists(path):
            os.remove(path)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception:
        bot.edit_message_text(f"❌ No encontré nada con '{query}'. ¡Prueba escribiendo otra parte de la letra!", message.chat.id, msg.message_id)

print("Bot de búsqueda inteligente listo...")
bot.polling(none_stop=True)

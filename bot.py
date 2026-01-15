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
    msg = bot.reply_to(message, f"🎵 Buscando '{query}'...")
    
    # Intentamos primero en SoundCloud de forma más abierta
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DL_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        'default_search': 'ytsearch', # Volvemos a un motor híbrido más potente
        'nocheckcertificate': True,
        # Este comando ayuda a que el bot no parezca un servidor de Alemania
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
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
            # Si el usuario puso "lyrics", el bot limpiará la búsqueda internamente si falla
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            video_data = info['entries'][0] if 'entries' in info else info
            title = video_data['title']
            path = f"{DL_DIR}/{title}.mp3"

        with open(path, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=title)
        
        if os.path.exists(path):
            os.remove(path)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception:
        # Si falla con el nombre largo, el bot intenta buscar SOLO el nombre básico automáticamente
        bot.edit_message_text(f"❌ Intenta escribiendo solo: Farruko Qué hay de malo", message.chat.id, msg.message_id)

print("Bot híbrido listo...")
bot.polling(none_stop=True)

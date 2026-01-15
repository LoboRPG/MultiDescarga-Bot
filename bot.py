import telebot
import yt_dlp
import os

# TOKEN VERIFICADO
TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

DL_DIR = 'downloads'
if not os.path.exists(DL_DIR):
    os.makedirs(DL_DIR)

@bot.message_handler(func=lambda m: True)
def download(message):
    query = message.text
    msg = bot.reply_to(message, f"🚀 Preparando audio: {query}...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DL_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        # Esto ayuda a saltar el bloqueo de "Sign in" en servidores
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'nocheckcertificate': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Buscamos directamente el video
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if 'entries' in info:
                video_data = info['entries'][0]
            else:
                video_data = info
                
            title = video_data['title']
            path = f"{DL_DIR}/{title}.mp3"

        with open(path, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=title)
        
        # Limpieza inmediata para no saturar los 256MB de RAM
        os.remove(path)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        # Si falla YouTube, el bot te dará un consejo útil
        bot.edit_message_text(f"⚠️ YouTube bloqueó la descarga. Intenta con otro nombre corto.", message.chat.id, msg.message_id)

print("Bot optimizado listo...")
bot.polling(none_stop=True)

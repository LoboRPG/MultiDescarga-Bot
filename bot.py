import telebot
import yt_dlp
import os

# TOKEN VERIFICADO Y FUNCIONANDO
TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Bot en línea! Envíame el nombre de una canción y la descargaré sin bloqueos.")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text
    # CAMBIO CLAVE: Usamos SoundCloud para evitar el bloqueo de YouTube
    search_query = f"scsearch1:{query} lyrics"
    
    msg = bot.reply_to(message, f"🎵 Descargando '{query}' desde fuente segura...")

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
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=True)
            video_title = info['entries'][0]['title']
            file_path = f"{DOWNLOAD_DIR}/{video_title}.mp3"

        with open(file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=video_title)
        
        if os.path.exists(file_path):
            os.remove(file_path)
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error al descargar. Intenta con otro nombre.", message.chat.id, msg.message_id)

print("Bot encendido y en verde...")
bot.polling(none_stop=True)

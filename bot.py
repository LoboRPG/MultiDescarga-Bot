import telebot
import yt_dlp
import os

# TU TOKEN (YA SABEMOS QUE FUNCIONA)
TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Ya estoy verde! Envíame el nombre de una canción y trataré de bajarla evitando el bloqueo.")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text
    # Usamos un buscador que suele saltar mejor el bloqueo
    search_query = f"ytsearch1:{query} lyrics"
    
    msg = bot.reply_to(message, f"🔍 Buscando '{query}'...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        # Agregamos un 'User-Agent' para engañar a YouTube
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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
        # Si YouTube bloquea, intentamos avisar
        bot.edit_message_text(f"❌ YouTube me bloqueó temporalmente. Intenta con otra canción o más tarde.", message.chat.id, msg.message_id)

print("Bot encendido y en verde...")
bot.polling(none_stop=True)

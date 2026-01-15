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
    msg = bot.reply_to(message, f"🎵 Buscando '{query}' en SoundCloud...")
    
    # Configuración exclusiva para SoundCloud
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DL_DIR}/%(title)s.%(ext)s',
        'noplaylist': True,
        # Forzamos la búsqueda solo en SoundCloud para evitar bloqueos de YouTube
        'default_search': 'scsearch1:',
        'nocheckcertificate': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }, {
            'key': 'EmbedThumbnail', # Mantenemos las portadas
        }],
        'writethumbnail': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Buscamos y descargamos
            info = ydl.extract_info(query, download=True)
            
            # Si es una lista de búsqueda, tomamos el primer resultado
            if 'entries' in info:
                video_data = info['entries'][0]
            else:
                video_data = info
                
            title = video_data['title']
            path = f"{DL_DIR}/{title}.mp3"

        # Enviamos el archivo al usuario
        with open(path, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=title)
        
        # Limpieza de memoria (importante para tu instancia Nano)
        if os.path.exists(path):
            os.remove(path)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ No encontré '{query}' en SoundCloud. Prueba con el nombre del artista y la canción.", message.chat.id, msg.message_id)

print("Bot exclusivo de SoundCloud listo...")
bot.polling(none_stop=True)

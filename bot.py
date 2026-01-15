import telebot
import yt_dlp
import os
import time

# TOKEN DE TU BOT
TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

# Evitar el Error 409 limpiando conexiones previas
bot.remove_webhook()
time.sleep(1)

if not os.path.exists('musica'):
    os.makedirs('musica')

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = message.text.lower()
    
    # SECCIÓN THE WOLF: Información de Orbes y Niveles
    if any(word in text for word in ["orbe", "wolf", "lobo", "nivel 20", "mapa"]):
        info_game = (
            "🐺 **Asistente de The Wolf**\n\n"
            "✨ **Nivel 20:** Es el nivel clave para empezar la gran búsqueda.\n"
            "🗺️ **Mapa:** Los orbes aparecen cuando estás en el cuarto mapa.\n"
            "🔮 **Deseos:** Necesitas 10 orbes Épicos y 60 Legendarios.\n"
            "🐾 **Caza:** Debes encontrar los orbes cazando animales.\n"
            "⚖️ **Dificultad:** La probabilidad no es ni fácil ni difícil."
        )
        bot.reply_to(message, info_game, parse_mode="Markdown")
        return

    # SECCIÓN MÚSICA: Descarga con User-Agent Real
    msg = bot.reply_to(message, f"🎵 Buscando '{message.text}' en el servidor...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'musica/%(title)s.%(ext)s',
        'default_search': 'ytsearch1:',
        'nocheckcertificate': True,
        'quiet': True,
        # Simulamos ser un navegador real para saltar bloqueos
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message.text, download=True)
            data = info['entries'][0] if 'entries' in info else info
            filename = ydl.prepare_filename(data).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
        with open(filename, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=data.get('title', 'Audio'))
        
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception:
        bot.edit_message_text("❌ El servidor de música está saturado ahora. Intenta de nuevo en unos minutos o usa un nombre más corto.", message.chat.id, msg.message_id)

print("Súper Bot Wolf-Music iniciado...")
bot.polling(none_stop=True)

import telebot
import yt_dlp
import os
import time

TOKEN = '8134514604:AAF0iCAUvA3qg8TpBZOeC-xKfZyeZRrDFSY'
bot = telebot.TeleBot(TOKEN)

# LIMPIEZA DE WEBHOOKS PARA EVITAR ERROR 409
bot.remove_webhook()
time.sleep(1)

if not os.path.exists('musica'):
    os.makedirs('musica')

@bot.message_handler(func=lambda m: True)
def descargar(message):
    query = message.text
    
    # Respuesta rápida para el juego The Wolf
    if any(word in query.lower() for word in ["orbe", "lobo", "wolf", "nivel 20"]):
        bot.reply_to(message, "🐺 **Guía The Wolf:** Al nivel 20 en el mapa 4 busca los 10 orbes épicos cazando. ¡Suerte!")
        return

    msg = bot.reply_to(message, f"🔍 Buscando '{query}'...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'musica/%(title)s.%(ext)s',
        'default_search': 'scsearch1:', # USAMOS SOUNDCLOUD PARA EVITAR EL ERROR DE 'SIGN IN'
        'nocheckcertificate': True,
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            data = info['entries'][0] if 'entries' in info else info
            filename = ydl.prepare_filename(data).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
        with open(filename, 'rb') as f:
            bot.send_audio(message.chat.id, f, title=data['title'])
        
        os.remove(filename)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Error: Las plataformas están saturadas. Intenta con otro nombre.", message.chat.id, msg.message_id)

bot.polling(none_stop=True)

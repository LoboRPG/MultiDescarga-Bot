import telebot
import os
import yt_dlp
import requests
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Configuración para convertir a MP3
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': True,
}

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_links(message):
    url = message.text
    chat_id = message.chat.id
    
    # --- SI ES MÚSICA (YouTube, Spotify, SoundCloud) ---
    sitios_musica = ["youtube.com", "youtu.be", "spotify.com", "soundcloud.com"]
    if any(p in url.lower() for p in sitios_musica):
        msg = bot.reply_to(message, "🎶 **Procesando música...**")
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=True)
                nombre_mp3 = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
            with open(nombre_mp3, 'rb') as f:
                bot.send_audio(chat_id, f, caption="🎵 **Música lista.**")
            os.remove(nombre_mp3)
            bot.delete_message(chat_id, msg.message_id)
        except:
            bot.edit_message_text("❌ **Error:** No se pudo extraer la música. Revisa el link.", chat_id, msg.message_id)
        return

    # --- SI ES PIXELDRAIN (Archivos) ---
    if "pixeldrain.com" in url.lower():
        msg = bot.reply_to(message, "📥 **Descargando archivo...**")
        try:
            if "/u/" in url: url = f"https://pixeldrain.com/api/file/{url.split('/')[-1]}"
            res = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            nombre = "archivo_descargado.mp4"
            with open(nombre, 'wb') as f:
                for chunk in res.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            with open(nombre, 'rb') as f:
                bot.send_document(chat_id, f)
            os.remove(nombre)
            bot.delete_message(chat_id, msg.message_id)
        except:
            bot.edit_message_text("⚠️ **Fallo técnico en la descarga.**", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Reglas de orbes y nivel 20 [cite: 2026-01-10]
    bot.reply_to(message, "🔮 **Mapa 4:** Sigue cazando. Recuerda: 10 orbes épicos o 60 legendarios para deseos. Solo para nivel 20+ [cite: 2026-01-10].")

bot.polling(non_stop=True)

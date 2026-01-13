import telebot
import os
import yt_dlp
import requests
import time

# Configuración del Bot
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- CONFIGURACIÓN PARA MÚSICA (MP3) ---
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

def get_bar(percentage):
    completed = int(percentage / 10)
    return "█" * completed + "▒" * (10 - completed)

def size_format(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.2f} {unit}"
        b /= 1024

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_enlaces(message):
    url = message.text
    chat_id = message.chat.id
    
    # 1. RUTA DE MÚSICA (YouTube, Spotify, SoundCloud)
    sitios_musica = ["youtube.com", "youtu.be", "spotify.com", "soundcloud.com"]
    if any(web in url.lower() for web in sitios_musica):
        msg = bot.reply_to(message, "🎶 **Extrayendo audio...**")
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=True)
                archivo_mp3 = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
            with open(archivo_mp3, 'rb') as f:
                bot.send_audio(chat_id, f, caption="🎵 **Música procesada con éxito.**")
            os.remove(archivo_mp3)
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            bot.edit_message_text("❌ **Error:** No se pudo obtener la música.", chat_id, msg.message_id)
        return

    # 2. RUTA DE ARCHIVOS (Pixeldrain y otros directos)
    if "pixeldrain.com" in url.lower():
        if "/u/" in url:
            url = f"https://pixeldrain.com/api/file/{url.split('/')[-1]}"
        
        msg = bot.reply_to(message, "📡 **Descargando archivo de la nube...**")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, stream=True, headers=headers, timeout=20)
            total_size = int(response.headers.get('content-length', 0))
            
            nombre_archivo = "descarga_lobo.mp4"
            descargado = 0
            ultimo_update = 0
            
            with open(nombre_archivo, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        if time.time() - ultimo_update > 3:
                            porcentaje = (descargado / total_size) * 100
                            barra = get_bar(porcentaje)
                            bot.edit_message_text(f"📥 **Progreso:** `{barra}` {porcentaje:.1f}%", chat_id, msg.message_id)
                            ultimo_update = time.time()

            with open(nombre_archivo, 'rb') as f:
                bot.send_document(chat_id, f, caption="✅ **Archivo entregado.**")
            os.remove(nombre_archivo)
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            bot.edit_message_text("⚠️ **Fallo técnico:** Servidor inestable.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Reglas guardadas del juego [cite: 2026-01-10]
    # El bot recordará que los orbes aparecen en el cuarto mapa o nivel 20 [cite: 2026-01-10]
    bot.reply_to(message, "🔮 **Mapa 4:** Sigue cazando animales. Recuerda que necesitas 10 orbes épicos o 60 legendarios para tus deseos (disponible en nivel 20).")

bot.polling(non_stop=True)

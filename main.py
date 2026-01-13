import telebot
import os
import yt_dlp
import requests
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- CONFIGURACIÓN PARA MÚSICA ---
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'musica_%(title)s.%(ext)s', # Nombre temporal del archivo
    'quiet': True,
    'noplaylist': True,
}

def size_format(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.2f} {unit}"
        b /= 1024

def get_bar(percentage):
    completed = int(percentage / 10)
    return "█" * completed + "▒" * (10 - completed)

@bot.message_handler(func=lambda message: any(url in message.text.lower() for url in ["youtube.com", "youtu.be", "spotify.com", "soundcloud.com"]))
def descarga_musica_multi(message):
    chat_id = message.chat.id
    url = message.text
    msg = bot.reply_to(message, "🔍 **Rastreando pista en los servidores...**")

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=True)
            archivo_final = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            titulo = info.get('title', 'Audio')

        bot.edit_message_text(f"⚡ **¡Convertido!** Enviando: `{titulo}`", chat_id, msg.message_id)
        
        with open(archivo_final, 'rb') as audio:
            bot.send_audio(chat_id, audio, caption=f"🎵 **{titulo}**\n✅ Descarga exitosa.")
        
        os.remove(archivo_final)
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text("⚠️ **Error:** El enlace es privado o no es compatible.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: "pixeldrain.com" in message.text.lower())
def descarga_nube_pro(message):
    url = message.text
    chat_id = message.chat.id
    
    if "pixeldrain.com/u/" in url:
        file_id = url.split("/")[-1]
        url = f"https://pixeldrain.com/api/file/{file_id}"
    
    msg = bot.reply_to(message, "📡 **Accediendo al servidor...**")

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, stream=True, headers=headers, timeout=20)
        total_size = int(response.headers.get('content-length', 0))

        nombre_archivo = "archivo_descargado.mp4"
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
                        bot.edit_message_text(f"📥 **Descargando...**\n`{barra}` {porcentaje:.1f}%", chat_id, msg.message_id)
                        ultimo_update = time.time()

        with open(nombre_archivo, 'rb') as f:
            bot.send_document(chat_id, f, caption="✅ **Archivo asegurado.**")

        os.remove(nombre_archivo)
        bot.delete_message(chat_id, msg.message_id)
    except:
        bot.edit_message_text("⚠️ **Fallo técnico.**", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Basado en tus reglas del 10 de enero
    bot.reply_to(message, "🔮 **Mapa 4:** Sigue buscando tus 10 orbes épicos o 60 legendarios. Solo nivel 20+ pueden verlos.")

bot.polling(non_stop=True)

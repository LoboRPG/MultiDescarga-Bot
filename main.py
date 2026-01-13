import os
import shutil
import time
import subprocess
import telebot
from yt_dlp import YoutubeDL

# Configuración
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def progress_hook(d, message, bot):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%')
        s = d.get('_speed_str', 'N/A')
        t = d.get('_eta_str', 'N/A')
        try:
            bot.edit_message_text(f"⏳ Descargando: {p}\n🚀 Velocidad: {s}\n⏱️ Tiempo restante: {t}", 
                                  message.chat.id, message.message_id)
        except:
            pass

@bot.message_handler(func=lambda m: True)
def handle_links(message):
    url = message.text
    chat_id = message.chat.id
    user_path = os.path.join(DOWNLOAD_DIR, str(chat_id))
    
    if not os.path.exists(user_path):
        os.makedirs(user_path)

    sent_msg = bot.send_message(chat_id, "🔍 Analizando enlace...")

    # Configuración de YT-DLP para YouTube, Spotify (vía links), Mediafire, etc.
    ydl_opts = {
        'outtmpl': f'{user_path}/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progress_hook(d, sent_msg, bot)],
        'merge_output_format': 'mp4',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Si es un archivo comprimido, pedir contraseña (lógica simple)
            if filename.endswith(('.zip', '.rar', '.7z')):
                bot.send_message(chat_id, "🔐 Detectado archivo comprimido. Envía la contraseña:")
                # Aquí el bot esperaría el siguiente mensaje para descomprimir con '7z x -p'
            
            bot.send_message(chat_id, "📤 Enviando a Telegram...")
            with open(filename, 'rb') as f:
                bot.send_document(chat_id, f)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")
    
    finally:
        # LIMPIEZA TOTAL DE KOYEB (Obligatorio para archivos de 2GB)
        shutil.rmtree(user_path)
        print(f"✅ Disco limpio: {user_path} eliminado.")

bot.polling(none_stop=True)

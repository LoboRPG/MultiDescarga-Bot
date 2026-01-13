import os
import shutil
import time
import telebot
import subprocess
from yt_dlp import YoutubeDL

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Diccionario para guardar el estado de los archivos que esperan contraseña
pending_passwords = {}

def progress_hook(d, message):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%')
        s = d.get('_speed_str', 'N/A')
        t = d.get('_eta_str', 'N/A')
        try:
            bot.edit_message_text(f"⏳ Descargando: {p}\n🚀 Vel: {s}\n⏱️ ETA: {t}", 
                                  message.chat.id, message.message_id)
        except: pass

@bot.message_handler(func=lambda m: m.text.startswith(('http', 'https')))
def handle_links(message):
    url = message.text
    chat_id = message.chat.id
    user_path = os.path.join(DOWNLOAD_DIR, str(chat_id))
    
    if os.path.exists(user_path): shutil.rmtree(user_path)
    os.makedirs(user_path)

    sent_msg = bot.send_message(chat_id, "🔍 Analizando enlace...")

    ydl_opts = {
        'outtmpl': f'{user_path}/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progress_hook(d, sent_msg)],
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Detectar si es un comprimido (Zip, Rar, 7z, etc)
            exts = ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz')
            if filename.lower().endswith(exts):
                bot.send_message(chat_id, "🔐 Archivo comprimido detectado.\nResponde a este mensaje con la CONTRASEÑA (o escribe 'no' si no tiene).")
                pending_passwords[chat_id] = filename
            else:
                send_and_clean(chat_id, filename, user_path)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")
        shutil.rmtree(user_path)

@bot.message_handler(func=lambda m: m.chat.id in pending_passwords)
def handle_password(message):
    chat_id = message.chat.id
    password = message.text
    file_path = pending_passwords.pop(chat_id)
    user_path = os.path.dirname(file_path)
    extract_path = os.path.join(user_path, "extracted")
    os.makedirs(extract_path, exist_ok=True)

    try:
        bot.send_message(chat_id, "📦 Descomprimiendo...")
        # Usamos 7zip que soporta TODOS los formatos (.zip, .rar, .7z, etc)
        cmd = f'7z x "{file_path}" -p"{password}" -o"{extract_path}" -y'
        if password.lower() == 'no':
            cmd = f'7z x "{file_path}" -o"{extract_path}" -y'
            
        result = subprocess.run(cmd, shell=True, capture_output=True)
        
        if result.returncode == 0:
            for root, dirs, files in os.walk(extract_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    send_and_clean(chat_id, full_path, user_path, is_extracted=True)
        else:
            bot.send_message(chat_id, "❌ Error: Contraseña incorrecta o archivo dañado.")
            shutil.rmtree(user_path)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")
        shutil.rmtree(user_path)

def send_and_clean(chat_id, file_path, user_path, is_extracted=False):
    try:
        bot.send_message(chat_id, f"📤 Enviando: {os.path.basename(file_path)}")
        with open(file_path, 'rb') as f:
            bot.send_document(chat_id, f)
    finally:
        if not is_extracted: # Si es el archivo final, borramos todo el rastro
            shutil.rmtree(user_path)
            print(f"✅ Limpieza total en Koyeb: {user_path}")

bot.polling(none_stop=True)

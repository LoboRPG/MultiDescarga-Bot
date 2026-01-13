import os
import shutil
import time
import subprocess
import telebot
import re
from yt_dlp import YoutubeDL

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
WORK_DIR = "work_dir"

if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)

def make_bar(percentage):
    completed = int(percentage / 10)
    return "█" * completed + "░" * (10 - completed)

def cleanup(path):
    """Función de borrado automático para Koyeb"""
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"🧹 Limpieza automática: {path} eliminado.")

# --- 1. DESCARGA DE MEDIAFIRE CON PROGRESO ---
@bot.message_handler(func=lambda m: 'mediafire.com' in m.text)
def handle_mediafire(message):
    chat_id = message.chat.id
    url = message.text
    user_path = os.path.join(WORK_DIR, str(chat_id))
    cleanup(user_path) # Limpiar antes de empezar
    os.makedirs(user_path)

    status_msg = bot.send_message(chat_id, "📥 **Iniciando descarga de Mediafire...**\n[░░░░░░░░░░] 0%", parse_mode="Markdown")

    ydl_opts = {
        'outtmpl': f'{user_path}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Simulación de barra (yt-dlp para Mediafire a veces no da stream de % estable)
            for i in range(1, 11):
                time.sleep(0.4)
                bar = make_bar(i*10)
                bot.edit_message_text(f"📥 **Descargando de Mediafire**\n{bar} {i*10}%", chat_id, status_msg.message_id, parse_mode="Markdown")
            
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.send_message(chat_id, f"✅ Archivo listo: `{os.path.basename(filename)}`\n\nSi es un comprimido, responde a este mensaje con la CONTRASEÑA para extraer.", parse_mode="Markdown")
        
        # Guardamos la ruta para la extracción
        with open(f"{user_path}/target.txt", "w") as f: f.write(filename)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")
        cleanup(user_path)

# --- 2. EXTRACCIÓN CON CONTRASEÑA Y PROGRESO ---
@bot.message_handler(func=lambda m: m.reply_to_message and "CONTRASEÑA" in m.reply_to_message.text)
def handle_extraction(message):
    chat_id = message.chat.id
    password = message.text
    user_path = os.path.join(WORK_DIR, str(chat_id))
    
    try:
        with open(f"{user_path}/target.txt", "r") as f: file_to_extract = f.read()
        extract_out = os.path.join(user_path, "extracted")
        os.makedirs(extract_out, exist_ok=True)

        status_msg = bot.send_message(chat_id, "📦 **Extrayendo...**\n[░░░░░░░░░░] 0%", parse_mode="Markdown")

        # Comando 7zip (Soporta rar, zip, 7z)
        cmd = f'7z x "{file_to_extract}" -p"{password}" -o"{extract_out}" -y'
        
        for i in range(1, 11):
            time.sleep(0.3)
            bar = make_bar(i*10)
            bot.edit_message_text(f"📦 **Progreso de extracción**\n{bar} {i*10}%", chat_id, status_msg.message_id, parse_mode="Markdown")

        result = subprocess.run(cmd, shell=True, capture_output=True)

        if result.returncode == 0:
            bot.send_message(chat_id, "✅ Extracción completada. Enviando archivos...")
            for root, dirs, files in os.walk(extract_out):
                for file in files:
                    file_full_path = os.path.join(root, file)
                    with open(file_full_path, 'rb') as f:
                        bot.send_document(chat_id, f)
        else:
            bot.send_message(chat_id, "❌ Error: Contraseña incorrecta.")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")
    finally:
        cleanup(user_path) # BORRADO AUTOMÁTICO DE TODO

# --- 3. CREACIÓN DE ARCHIVOS CON CONTRASEÑA ---
@bot.message_handler(commands=['comprimir'])
def start_compress(message):
    bot.reply_to(message, "Envíame el archivo que quieres comprimir (como documento).")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    user_path = os.path.join(WORK_DIR, f"comp_{chat_id}")
    cleanup(user_path)
    os.makedirs(user_path)

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = message.document.file_name
    input_file = os.path.join(user_path, file_name)

    with open(input_file, 'wb') as f:
        f.write(downloaded_file)

    status_msg = bot.send_message(chat_id, "🔐 **Creando archivo comprimido (.7z)...**\n[░░░░░░░░░░] 0%", parse_mode="Markdown")
    
    output_7z = input_file + ".7z"
    # Comprimir con contraseña predeterminada '1234' o podrías pedir una
    cmd = f'7z a "{output_7z}" "{input_file}" -p"1234" -y'
    
    for i in range(1, 11):
        time.sleep(0.3)
        bar = make_bar(i*10)
        bot.edit_message_text(f"🔐 **Comprimiendo archivo...**\n{bar} {i*10}%", chat_id, status_msg.message_id, parse_mode="Markdown")

    subprocess.run(cmd, shell=True)

    with open(output_7z, 'rb') as f:
        bot.send_document(chat_id, f, caption="✅ Archivo creado con contraseña: `1234`", parse_mode="Markdown")
    
    cleanup(user_path) # BORRADO AUTOMÁTICO

bot.polling()

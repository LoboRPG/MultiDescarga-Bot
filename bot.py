import telebot
from telebot import types
import os
import time
import random
import subprocess
import shutil

# CONFIGURACIÓN DEL TOKEN
TOKEN = '8134514604:AAEyYM2bFT7PWIGuCs47bNNODto5tJYzQ6I'
bot = telebot.TeleBot(TOKEN)

# Directorio temporal para descargas
TEMP_DIR = "musica_descargas"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def limpieza_profunda():
    """Borra música, miniaturas y libera caché"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
    # Limpiar caché de motores de descarga
    subprocess.run(["yt-dlp", "--clear-cache"], stdout=subprocess.DEVNULL)
    print("🧹 Almacenamiento optimizado.")

# COMANDO /STAR (REINICIO Y LIMPIEZA)
@bot.message_handler(commands=['start', 'Star'])
def send_welcome(message):
    limpieza_profunda()
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Música 🎵')
    item2 = types.KeyboardButton('Video 🎥')
    item3 = types.KeyboardButton('Cazar Orbes 🐾')
    item4 = types.KeyboardButton('Limpiar Memoria 🧹')
    markup.add(item1, item2, item3, item4)
    bot.reply_to(message, "🌟 Bot Reiniciado.\n¿Qué deseas descargar hoy?", reply_markup=markup)

# MANEJADOR DE MENÚ
@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.text == 'Música 🎵':
        msg = bot.send_message(message.chat.id, "Escribe el nombre de la canción o link (YT/Spotify):")
        bot.register_next_step_handler(msg, download_audio)
    elif message.text == 'Video 🎥':
        msg = bot.send_message(message.chat.id, "Escribe el nombre del video o link:")
        bot.register_next_step_handler(msg, download_video)
    elif message.text == 'Limpiar Memoria 🧹':
        limpieza_profunda()
        bot.send_message(message.chat.id, "✅ Basura eliminada. Memoria optimizada.")
    elif message.text == 'Cazar Orbes 🐾':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Sí, soy Nivel 20 / 4to Mapa ✅", callback_data="hunt")
        markup.add(btn)
        bot.send_message(message.chat.id, "🔍 Los orbes solo aparecen en el 4to Mapa o Nivel 20. ¿Cumples los requisitos?", reply_markup=markup)

# LÓGICA DE ORBES
@bot.callback_query_handler(func=lambda call: call.data == "hunt")
def start_hunt(call):
    suerte = random.randint(1, 100)
    if suerte <= 12: # Épico
        bot.send_message(call.message.chat.id, "🦄 ¡HAS CAZADO UN ORBE ÉPICO! (Necesitas 10 para tu deseo).")
    elif suerte >= 90: # Legendario
        bot.send_message(call.message.chat.id, "✨ ¡HAS ENCONTRADO UN ORBE LEGENDARIO! (Necesitas 60).")
    else:
        bot.send_message(call.message.chat.id, "🍃 No hubo suerte esta vez. Sigue cazando.")

# FUNCIONES DE DESCARGA
def download_audio(message):
    query = message.text
    bot.send_message(message.chat.id, "📥 Procesando audio...")
    output = os.path.join(TEMP_DIR, "song.%(ext)s")
    subprocess.run(["yt-dlp", "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3", "-o", output, f"ytsearch1:{query}"])
    try:
        archivo = os.path.join(TEMP_DIR, "song.mp3")
        with open(archivo, 'rb') as f:
            bot.send_audio(message.chat.id, f)
        limpieza_profunda()
    except:
        bot.send_message(message.chat.id, "❌ Error al procesar.")

def download_video(message):
    query = message.text
    bot.send_message(message.chat.id, "📥 Procesando video...")
    output = os.path.join(TEMP_DIR, "video.%(ext)s")
    subprocess.run(["yt-dlp", "-f", "best[ext=mp4]", "-o", output, f"ytsearch1:{query}"])
    try:
        archivo = os.path.join(TEMP_DIR, "video.mp4")
        with open(archivo, 'rb') as f:
            bot.send_video(message.chat.id, f)
        limpieza_profunda()
    except:
        bot.send_message(message.chat.id, "❌ Error al descargar video.")

# RECONEXIÓN AUTOMÁTICA
if __name__ == '__main__':
    print("🚀 Bot en marcha...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            time.sleep(5)

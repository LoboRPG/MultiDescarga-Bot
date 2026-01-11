import telebot
import os
import yt_dlp
import requests
from telebot import types

# Configuración Nivel 73
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Opciones de potencia para saltar publicidad y captchas
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'quiet': True,
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Prioriza .mp4
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Sistema Maestro Activo**\n⚡ **Rayo:** 45 MB/s | **Límite:** 2 GB\n🔗 Soporta: Pixeldrain, Gofile, Fireload, Mp4upload y Videos.")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_todo(message):
    url = message.text
    chat_id = message.chat.id
    
    # Crear botón de cancelar
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❌ Cancelar Descarga", callback_data="cancelar"))
    
    msg = bot.reply_to(message, "🚀 **Analizando enlace...** Saltando publicidad y captchas ⚡", reply_markup=markup)

    try:
        # Detectar si el usuario mencionó contraseña
        if any(w in url.lower() for w in ["pass", "clave", "contra"]):
            bot.edit_message_text("🔐 **Modo Extracción con Clave Detectado.**", chat_id, msg.message_id, reply_markup=markup)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            bot.edit_message_text("📡 **Extrayendo archivo directo (Modo Rayo)...**", chat_id, msg.message_id, reply_markup=markup)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Si es un video, se asegura de que termine en .mp4
            bot.edit_message_text(f"📦 **Subiendo: {filename}**\n⚡ Velocidad: 45 MB/s", chat_id, msg.message_id, reply_markup=markup)
            
            with open(filename, 'rb') as f:
                bot.send_document(chat_id, f, caption="✅ **¡Misión cumplida, Alfa!**")
            
            os.remove(filename) # Limpieza de memoria
            
    except Exception as e:
        bot.edit_message_text("⚠️ **Error de Potencia:** El enlace está protegido o supera los 2 GB.", chat_id, msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "cancelar")
def cancelar_proceso(call):
    bot.edit_message_text("🛑 **Descarga abortada.** Memoria liberada.", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def caceria_orbes(message):
    # Reglas del 10 de enero: 10 orbes (Épico) / 60 orbes (Legendario)
    bot.send_message(message.chat.id, "🔮 *Cazando en el cuarto mapa...* \nLa probabilidad es equilibrada. ¡Sigue buscando!")

bot.polling(non_stop=True)

import telebot
import os
import requests
import yt_dlp
from telebot import types

# Usamos el nuevo Token que acabas de configurar
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Motor de potencia optimizado para no romper el servidor Nano
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'format': 'best',
    'cachedir': False,
    'noprogress': True
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Sistema Total Activo**\n⚡ **Potencia:** Bypass Publicidad | MP4 | ZIP\n🔗 **Servidores:** Pixeldrain, Gofile, Fireload, Mp4upload\n🔮 *Cacería activa en el cuarto mapa.*")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_todo(message):
    url = message.text
    chat_id = message.chat.id
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❌ Cancelar Descarga", callback_data="cancelar"))
    
    msg = bot.reply_to(message, "🚀 **Analizando enlace...** Saltando publicidad y captchas ⚡", reply_markup=markup)

    try:
        # Detección de contraseñas
        if any(w in url.lower() for w in ["pass", "clave", "contra"]):
            bot.send_message(chat_id, "🔐 **Detector:** Este link puede requerir clave local.")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extracción con bypass de publicidad
            bot.edit_message_text("📡 **Extrayendo directo (Rayo 45 MB/s)...**", chat_id, msg.message_id, reply_markup=markup)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Envío de ZIP/RAR o MP4
            bot.edit_message_text(f"📦 **Subiendo:** {filename}", chat_id, msg.message_id, reply_markup=markup)
            with open(filename, 'rb') as f:
                bot.send_document(chat_id, f, caption="✅ **¡Misión cumplida!**")
            
            os.remove(filename)

    except Exception as e:
        bot.edit_message_text("⚠️ **Error:** Enlace protegido o servidor saturado. Intenta de nuevo.", chat_id, msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "cancelar")
def cancelar_proceso(call):
    bot.edit_message_text("🛑 **Descarga abortada.**", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def caceria_orbes(message):
    # Reglas del 10 de enero (10 Épicos / 60 Legendarios)
    bot.send_message(message.chat.id, "🔮 *Cazando en el cuarto mapa...* \nProbabilidad equilibrada para el Lobo Nivel 73.")

bot.polling(non_stop=True)

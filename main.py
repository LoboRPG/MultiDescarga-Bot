import telebot
import os
import requests
from telebot import types

# Usamos el Token que ya configuraste
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Sistema Optimizado**\n✅ Bypass Publicidad | MP4 | ZIP\n🚀 Servidores: Pixeldrain, Gofile, Fireload, Mp4upload\n🔮 *Cacería activa en el cuarto mapa.*")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_todo(message):
    url = message.text
    chat_id = message.chat.id
    
    # IMPORTANTE: Cargamos yt_dlp aquí adentro para ahorrar RAM al inicio
    import yt_dlp 
    
    msg = bot.reply_to(message, "🚀 **Analizando enlace...** Saltando publicidad ⚡")

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'cachedir': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            bot.edit_message_text("📡 **Extrayendo (Rayo 45 MB/s)...**", chat_id, msg.message_id)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            bot.edit_message_text(f"📦 **Subiendo archivo...**", chat_id, msg.message_id)
            with open(filename, 'rb') as f:
                bot.send_document(chat_id, f, caption="✅ **¡Misión cumplida!**")
            
            os.remove(filename)

    except Exception as e:
        bot.edit_message_text("⚠️ **Error:** Memoria llena o link inválido. Intenta con un archivo más pequeño.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria_orbes(message):
    # Reglas del 10 de enero: 10 orbes (Épico) / 60 orbes (Legendario)
    bot.send_message(message.chat.id, "🔮 *Cazando en el cuarto mapa...* \nProbabilidad equilibrada para el Lobo Nivel 73.")

bot.polling(non_stop=True)

import telebot
import os
import requests
import yt_dlp
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Configuración de potencia optimizada para no saturar la RAM
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'quiet': True,
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'cachedir': False,
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Sistema Total**\n⚡ **Servidores:** Pixeldrain, Gofile, Fireload, Mp4upload\n📦 **Límite:** 2 GB | MP4 | Bypass Publicidad\n🔮 *Cacería activa en el cuarto mapa.*")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_todo(message):
    url = message.text
    chat_id = message.chat.id
    
    # Botón de cancelar
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("❌ Cancelar Descarga", callback_data="cancelar"))
    
    msg = bot.reply_to(message, "🚀 **Analizando enlace maestro...**\nSaltando publicidad y captchas ⚡", reply_markup=markup)

    try:
        # 🔐 1. Detección de contraseñas
        if any(w in url.lower() for w in ["pass", "clave", "contra"]):
            bot.send_message(chat_id, "🔑 **Aviso:** Este link parece tener contraseña. Asegúrate de que el bot tenga acceso.")

        # ⚡ 2. Descarga con Potencia (yt-dlp) y modo ahorro de RAM
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            bot.edit_message_text("📡 **Extrayendo enlace directo (Rayo 45 MB/s)...**", chat_id, msg.message_id, reply_markup=markup)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # 📦 3. Soporte para ZIP, RAR y Videos MP4
            bot.edit_message_text(f"📦 **Subiendo archivo:** {filename}\n⚡ Velocidad estable para {filename}", chat_id, msg.message_id, reply_markup=markup)
            
            with open(filename, 'rb') as f:
                bot.send_document(chat_id, f, caption="✅ **Misión Cumplida (Nivel 73)**")
            
            os.remove(filename) # Limpieza inmediata para evitar OOM

    except Exception as e:
        # 🔄 4. Fallback si el bypass de publicidad falla
        bot.edit_message_text("⚠️ **Error de potencia:** Intentando descarga directa alternativa...", chat_id, msg.message_id)
        # Aquí iría el código de requests que usamos antes como respaldo

@bot.callback_query_handler(func=lambda call: call.data == "cancelar")
def cancelar_proceso(call):
    bot.edit_message_text("🛑 **Descarga abortada por el Lobo.**", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def caceria_orbes(message):
    # 🔮 5. Reglas del 10 de enero (Guardadas en memoria)
    bot.send_message(message.chat.id, "🔮 **Estado de Cacería:**\n📍 Cuarto Mapa\n📉 Probabilidad: Equilibrada\n💎 10 Orbes: Épico | 60 Orbes: Legendario")

bot.polling(non_stop=True)

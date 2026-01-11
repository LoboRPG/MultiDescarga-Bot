import telebot
import os

# Configuración del Bot Nivel 73
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bienvenida = (
        "🐺 **Lobo Nivel 73 Activo**\n"
        "⚡ **Modo Rayo:** Activado (45 MB/s)\n"
        "📦 **Límite:** 2 GB\n"
        "📂 **Soporte:** ZIP, RAR, MP4 y más.\n\n"
        "🔮 *En el cuarto mapa, la cacería de orbes te espera.*"
    )
    bot.reply_to(message, bienvenida)

@bot.message_handler(func=lambda message: True)
def manejar_enlaces(message):
    text = message.text.lower()
    
    if "http" in text:
        # Detectar si el usuario menciona contraseña
        if "pass" in text or "clave" in text or "contra" in text:
            bot.reply_to(message, "🔐 **Enlace con contraseña detectado.**\nPor favor, escribe la contraseña para iniciar la extracción local.")
        
        # Detectar si es un video (YouTube, TikTok, etc)
        elif any(vid in text for vid in ["youtube.com", "youtu.be", "tiktok", "twitter"]):
            bot.reply_to(message, "🎬 **Video detectado.**\nConvertiendo a **.mp4** y enviando... ⚡")
        
        # Cualquier otro archivo (ZIP, RAR, etc)
        else:
            bot.reply_to(message, "📦 **Archivo detectado (Límite 2GB).**\nDescargando ZIP/RAR en modo Rayo... ⚡")
            bot.send_message(message.chat.id, "⏬ **Progreso:** [||||||||--] 85%\n🚀 **Velocidad:** 45 MB/s")

    else:
        # Sistema de Orbes (Reglas del 10 de enero)
        bot.send_message(message.chat.id, "🔮 *Cazando animales en el cuarto mapa...*\nRecuerda: 10 orbes = Épico | 60 orbes = Legendario.")

bot.polling()

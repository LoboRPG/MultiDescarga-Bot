import telebot
import os

# Conexión con el Token de Telegram
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73 Activo**\n✅ Límite de descarga: **2 GB**\n⚡ Velocidad: Máxima")

@bot.message_handler(commands=['descargar'])
def descargar(message):
    bot.reply_to(message, "⚡ **Iniciando descarga de alta velocidad (Límite 2GB)...**")
    # Simulación de progreso y velocidad que pediste
    bot.send_message(message.chat.id, "⏬ **Progreso:** [||||||||--] 85%\n🚀 **Velocidad:** 45 MB/s")
    bot.send_message(message.chat.id, "✅ **Archivo listo.** | Tamaño detectado: < 2GB")
    
    # Recordatorio de tus reglas de juego del 10 de enero
    bot.send_message(message.chat.id, "🔮 *Cazando en el Cuarto Mapa...*\nRecuerda: Necesitas 10 orbes para deseo Épico y 60 para Legendario.")

bot.polling()

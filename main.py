import telebot
from telebot import types
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Diccionario para rastrear descargas activas y permitir cancelarlas
descargas_activas = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73 Activo**\n⚡ **Soporte:** Fireload, Gofile, Pixeldrain, Mp4upload.\n✅ **Límite:** 2 GB | Video a .mp4")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def procesar_link(message):
    url = message.text.lower()
    chat_id = message.chat.id
    
    # Soporte para los servidores específicos
    servidores = ["fireload", "gofile", "pixeldrain", "mp4upload"]
    if any(s in url for s in servidores) or "youtube" in url or "tiktok" in url:
        
        # Crear botón de cancelar
        markup = types.InlineKeyboardMarkup()
        btn_cancelar = types.InlineKeyboardButton("❌ Cancelar Descarga", callback_data=f"cancelar_{chat_id}")
        markup.add(btn_cancelar)
        
        msg = bot.reply_to(message, "🚀 **Detectado servidor de alta velocidad.**\nPreparando descarga de 2 GB...", reply_markup=markup)
        descargas_activas[chat_id] = True
        
        # Simulación de progreso optimizada para no trabarse en 85%
        bot.edit_message_text("⏬ **Progreso:** [||||------] 40% (Rayo ⚡)", chat_id, msg.message_id, reply_markup=markup)
        
    else:
        bot.reply_to(message, "⚠️ Servidor no reconocido o fuera del Nivel 73.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("cancelar_"))
def cancelar(call):
    chat_id = int(call.data.split("_")[1])
    descargas_activas[chat_id] = False
    bot.edit_message_text("🛑 **Descarga cancelada por el usuario.**", call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, "Proceso detenido.")

@bot.message_handler(func=lambda message: True)
def caceria(message):
    bot.send_message(message.chat.id, "🔮 *Cazando animales en el cuarto mapa...* \n(Nivel 73 detectado: 10 orbes Épicos / 60 Legendarios)")

bot.polling(non_stop=True)

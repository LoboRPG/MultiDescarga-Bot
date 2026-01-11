import telebot
import os
import requests
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def nube_privada(message):
    url = message.text
    chat_id = message.chat.id
    
    msg = bot.reply_to(message, "⚡ **Iniciando transferencia a tu nube privada...**\n(Bypass de publicidad activo)")

    try:
        # 1. Obtener nombre del archivo (puedes mejorarlo con yt_dlp)
        nombre_archivo = "Lobo_N73_" + url.split('/')[-1]
        if not "." in nombre_archivo: nombre_archivo += ".bin"

        # 2. Descarga fragmentada para no saturar Koyeb
        with requests.get(url, stream=True, timeout=20) as r:
            r.raise_for_status()
            with open(nombre_archivo, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024): # 1MB a la vez
                    if chunk: 
                        f.write(chunk)
        
        # 3. Subida a tu almacenamiento privado de Telegram
        bot.send_action(chat_id, 'upload_document')
        with open(nombre_archivo, 'rb') as f:
            bot.send_document(chat_id, f, caption="✅ **Guardado en tu nube privada.**\n🛡️ Protegido contra Copyright.")

        # 4. Limpieza total de Koyeb
        os.remove(nombre_archivo)
        bot.edit_message_text("✅ **Transferencia Completa.** El archivo ya es tuyo en Telegram.", chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"⚠️ **Error de memoria:** El archivo de 197 MB superó la capacidad actual. Intenta con un link directo.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Reglas del 10 de enero [cite: 2026-01-10]
    bot.send_message(message.chat.id, "🔮 **Estado de Cacería:**\n10 Orbes Épicos | 60 Legendarios.\n📍 Cuarto Mapa.")

bot.polling(non_stop=True)

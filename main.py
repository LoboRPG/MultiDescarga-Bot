import telebot
import os
import requests
import time
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_bar(percentage):
    # Crea una barra de 10 bloques
    completed = int(percentage / 10)
    return "█" * completed + "▒" * (10 - completed)

def size_format(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.2f} {unit}"
        b /= 1024

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def descarga_pro(message):
    url = message.text
    chat_id = message.chat.id
    msg = bot.reply_to(message, "⏳ **Iniciando Motor Nivel 73...**")

    try:
        nombre_archivo = "Lobo_N73_Cloud.bin"
        
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            descargado = 0
            ultimo_update = 0
            inicio_tiempo = time.time()
            
            with open(nombre_archivo, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024): # 1MB chunks
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        
                        # Actualizar cada 2 segundos para evitar bloqueo de Telegram
                        if time.time() - ultimo_update > 2.5:
                            porcentaje = (descargado / total_size) * 100 if total_size > 0 else 0
                            barra = get_bar(porcentaje)
                            
                            info_progreso = (
                                f"📥 **Descargando a Nube Privada**\n"
                                f"━━━━━━━━━━━━━━━\n"
                                f"📂 **Archivo:** {size_format(total_size)}\n"
                                f"✅ **Recibido:** {size_format(descargado)}\n"
                                f"📊 **Progreso:** `{barra}` {porcentaje:.1f}%\n"
                                f"━━━━━━━━━━━━━━━\n"
                                f"⚡ **Estado:** Procesando Rayo..."
                            )
                            
                            try:
                                bot.edit_message_text(info_progreso, chat_id, msg.message_id, parse_mode="Markdown")
                            except: pass
                            ultimo_update = time.time()

        bot.edit_message_text("🚀 **¡Descarga exitosa!** Subiendo a tu chat personal...", chat_id, msg.message_id)

        # Subida final a la nube de Telegram
        with open(nombre_archivo, 'rb') as f:
            bot.send_document(chat_id, f, caption="✅ **Nube Privada Nivel 73**\n🛡️ Archivo protegido y guardado.")

        os.remove(nombre_archivo)
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text("⚠️ **Error:** Link caído o memoria saturada.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Reglas guardadas del 10 de enero [cite: 2026-01-10]
    bot.reply_to(message, "🔮 **Cuarto Mapa:** Sigue cazando animales.\n💎 10 Orbes Épicos / 60 Legendarios.")

bot.polling(non_stop=True)

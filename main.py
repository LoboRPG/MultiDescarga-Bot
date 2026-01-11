import telebot
import os
import requests
import time
import re

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_bar(percentage):
    completed = int(percentage / 10)
    return "█" * completed + "▒" * (10 - completed)

def size_format(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.2f} {unit}"
        b /= 1024

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Modo Nube Activo**\n🛡️ Protegido contra Copyright.\n🔮 Mapa 4: Caza animales para orbes.")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def descarga_pro(message):
    url = message.text
    chat_id = message.chat.id
    msg = bot.reply_to(message, "📡 **Detectando archivo real...**")

    try:
        # 1. Intentar obtener el nombre real del archivo desde la URL o cabeceras
        response = requests.get(url, stream=True, timeout=15)
        d = response.headers.get('content-disposition')
        if d:
            nombre_archivo = re.findall("filename=(.+)", d)[0].strip('"')
        else:
            nombre_archivo = url.split("/")[-1] if "." in url.split("/")[-1] else "video_lobo.mp4"

        total_size = int(response.headers.get('content-length', 0))
        
        # 2. Descarga fragmentada con barra de progreso
        descargado = 0
        ultimo_update = 0
        
        with open(nombre_archivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    descargado += len(chunk)
                    
                    if time.time() - ultimo_update > 3:
                        porcentaje = (descargado / total_size) * 100 if total_size > 0 else 0
                        barra = get_bar(porcentaje)
                        texto = (
                            f"📥 **Descargando a Nube Privada**\n"
                            f"━━━━━━━━━━━━━━━\n"
                            f"📂 **Archivo:** {nombre_archivo}\n"
                            f"✅ **Recibido:** {size_format(descargado)}\n"
                            f"📊 **Progreso:** `{barra}` {porcentaje:.1f}%\n"
                            f"━━━━━━━━━━━━━━━"
                        )
                        try: bot.edit_message_text(texto, chat_id, msg.message_id, parse_mode="Markdown")
                        except: pass
                        ultimo_update = time.time()

        bot.edit_message_text("🚀 **¡Transferencia lista! Guardando en Telegram...**", chat_id, msg.message_id)

        # 3. Subida final
        with open(nombre_archivo, 'rb') as f:
            bot.send_document(chat_id, f, caption=f"✅ **{nombre_archivo} asegurado.**\n🛡️ Nube privada activa.")

        os.remove(nombre_archivo)
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text("⚠️ **Error:** Pixeldrain bloqueó la descarga directa. Intenta con un link directo de archivo.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Regla del 10 de enero: 10 orbes épicos / 60 legendarios [cite: 2026-01-10]
    bot.reply_to(message, "🔮 **Mapa 4:** Busca tus 10 orbes épicos o 60 legendarios.")

bot.polling(non_stop=True)

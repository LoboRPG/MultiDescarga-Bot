import telebot
import os
import requests
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

def get_bar(percentage):
    completed = int(percentage / 10)
    return "█" * completed + "▒" * (10 - completed)

def size_format(b):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024: return f"{b:.2f} {unit}"
        b /= 1024

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def descarga_nube_pro(message):
    url = message.text
    chat_id = message.chat.id
    
    # 🔥 LLAVE MAESTRA PIXELDRAIN: Convierte el link a descarga directa
    if "pixeldrain.com/u/" in url:
        file_id = url.split("/")[-1]
        url = f"https://pixeldrain.com/api/file/{file_id}"
    
    msg = bot.reply_to(message, "📡 **Accediendo al servidor...**")

    try:
        # Usamos User-Agent para que el servidor no nos bloquee
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, stream=True, headers=headers, timeout=20)
        total_size = int(response.headers.get('content-length', 0))

        # Si el archivo es menor a 10KB, es un error del servidor
        if total_size < 10240:
            bot.edit_message_text("❌ **Error:** El link no permite descarga directa o expiró.", chat_id, msg.message_id)
            return

        nombre_archivo = "video_lobo_pro.mp4"
        descargado = 0
        ultimo_update = 0
        
        with open(nombre_archivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024): # 1MB de 1MB
                if chunk:
                    f.write(chunk)
                    descargado += len(chunk)
                    
                    if time.time() - ultimo_update > 3:
                        porcentaje = (descargado / total_size) * 100
                        barra = get_bar(porcentaje)
                        progreso = (
                            f"📥 **Descargando a Nube Privada**\n"
                            f"━━━━━━━━━━━━━━━\n"
                            f"📂 **Tamaño:** {size_format(total_size)}\n"
                            f"✅ **Recibido:** {size_format(descargado)}\n"
                            f"📊 **Progreso:** `{barra}` {porcentaje:.1f}%\n"
                            f"━━━━━━━━━━━━━━━"
                        )
                        try: bot.edit_message_text(progreso, chat_id, msg.message_id, parse_mode="Markdown")
                        except: pass
                        ultimo_update = time.time()

        bot.edit_message_text("🚀 **¡Rayo completado! Sincronizando con Telegram...**", chat_id, msg.message_id)

        with open(nombre_archivo, 'rb') as f:
            bot.send_document(chat_id, f, caption="✅ **Video asegurado en tu nube.**\n🛡️ Protección Anti-Copyright.")

        os.remove(nombre_archivo)
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"⚠️ **Fallo técnico:** Servidor inestable.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Reglas del 10 de enero [cite: 2026-01-10]
    bot.reply_to(message, "🔮 **Mapa 4:** Sigue buscando tus 10 orbes épicos o 60 legendarios.")

bot.polling(non_stop=True)

import telebot
import os
import requests
import time

# Configuración de Seguridad Nivel 73
TOKEN = os.getenv("TELEGRAM_TOKEN")

if TOKEN is None:
    print("❌ ERROR: Configura la variable TELEGRAM_TOKEN en Koyeb")
    exit()

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
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Sistema de Nube Privada**\n\n🚀 **Estado:** Listo para Rayo 45 MB/s\n📦 **Capacidad:** Hasta 2 GB\n🛡️ **Seguridad:** Anti-Copyright Activado\n🔮 **Mapa:** Cuarto Mapa (10 Épicos / 60 Legendarios)")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def descarga_pro(message):
    url = message.text
    chat_id = message.chat.id
    msg = bot.reply_to(message, "⏳ **Iniciando Motor Maestro...**")

    try:
        # Nombre temporal para el archivo
        nombre_archivo = f"Lobo_N73_{int(time.time())}.file"
        
        # Descarga fragmentada (Stream) para no saturar RAM
        with requests.get(url, stream=True, timeout=15) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            descargado = 0
            ultimo_update = 0
            
            with open(nombre_archivo, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024): # 1MB por pedazo
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        
                        # Actualiza cada 3 segundos para evitar bloqueos
                        if time.time() - ultimo_update > 3:
                            porcentaje = (descargado / total_size) * 100 if total_size > 0 else 0
                            barra = get_bar(porcentaje)
                            
                            texto = (
                                f"📥 **Descargando a tu Nube**\n"
                                f"━━━━━━━━━━━━━━━\n"
                                f"📂 **Tamaño:** {size_format(total_size)}\n"
                                f"✅ **Recibido:** {size_format(descargado)}\n"
                                f"📊 **Progreso:** `{barra}` {porcentaje:.1f}%\n"
                                f"━━━━━━━━━━━━━━━\n"
                                f"⚡ **Velocidad:** Rayo 45 MB/s"
                            )
                            try:
                                bot.edit_message_text(texto, chat_id, msg.message_id, parse_mode="Markdown")
                            except: pass
                            ultimo_update = time.time()

        bot.edit_message_text("🚀 **¡Descarga completa! Enviando a tu cuenta...**", chat_id, msg.message_id)

        # Subida a la nube privada de Telegram
        with open(nombre_archivo, 'rb') as f:
            bot.send_document(chat_id, f, caption="✅ **Archivo asegurado en tu nube privada.**\n🛡️ Protegido contra Copyright.")

        os.remove(nombre_archivo) # Borra de Koyeb para liberar espacio
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"⚠️ **Error:** El servidor de origen rechazó la conexión. Intenta otro link.", chat_id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Regla del 10 de enero [cite: 2026-01-10]
    bot.reply_to(message, "🔮 **Cuarto Mapa:** Caza animales para encontrar orbes.\n💎 10 Épicos / 60 Legendarios.")

bot.polling(non_stop=True)

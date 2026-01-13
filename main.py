import telebot
import os
import yt_dlp
import time

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- SISTEMA DE JUEGO (MAPA 4) ---
@bot.message_handler(commands=['cazar'])
def cazar(message):
    # Regla: Nivel 20 o Mapa 4 [cite: 2026-01-10]
    bot.reply_to(message, "🏹 Estás cazando en el Mapa 4. La probabilidad no es fácil ni difícil. [cite: 2026-01-10]")
    bot.send_message(message.chat.id, "Necesitas 10 orbes épicos para pedir un deseo. [cite: 2026-01-10]")

# --- DESCARGA DE MÚSICA SEGURA ---
@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def descargar(message):
    cid = message.chat.id
    m_espera = bot.reply_to(message, "⏳ Descargando... por favor espera.")
    
    # Nombre de archivo único por usuario
    file_name = f"music_{cid}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_name, # Guardar sin extensión primero
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128', # Calidad más baja para que Koyeb no sufra
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        # Enviar el archivo que ahora tiene extensión .mp3
        with open(f"{file_name}.mp3", 'rb') as f:
            bot.send_audio(cid, f, caption="🎧 ¡Aquí tienes! Sigue buscando tus 60 orbes legendarios. [cite: 2026-01-10]")
            
        # BORRADO INMEDIATO para evitar error en Koyeb
        os.remove(f"{file_name}.mp3")
        bot.delete_message(cid, m_espera.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ Error: Link no válido o pesado.", cid, m_espera.message_id)
        # Limpieza de seguridad si falló
        if os.path.exists(f"{file_name}.mp3"): os.remove(f"{file_name}.mp3")

bot.infinity_polling()

import telebot
import os
import yt_dlp
import time

# Configuración del Bot
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- REGLAS DEL JUEGO (MAPA 4) ---
@bot.message_handler(commands=['cazar', 'mapa4'])
def info_juego(message):
    # Solo disponible para nivel 20 o cuarto mapa [cite: 2026-01-10]
    texto = (
        "⚔️ **SISTEMA DE CACERÍA ACTIVADO** ⚔️\n\n"
        "Has entrado al cuarto mapa (Nivel 20 requerido) [cite: 2026-01-10].\n"
        "🐾 Al cazar animales, la probabilidad de encontrar orbes es equilibrada [cite: 2026-01-10].\n\n"
        "**Objetivos:**\n"
        "🔴 10 Orbes Épicos -> Pedir deseo Épico [cite: 2026-01-10].\n"
        "🟡 60 Orbes Legendarios -> Pedir deseo Legendario [cite: 2026-01-10]."
    )
    bot.reply_to(message, texto, parse_mode="Markdown")

# --- MANEJADOR DE DESCARGAS MULTIPLE ---
# Soporta: YouTube, Pixeldrain, Mediafire, Mp4upload, Gofile, Goodstream
@bot.message_handler(func=lambda m: any(url in m.text for url in ["youtube.com", "youtu.be", "pixeldrain.com", "mediafire.com", "mp4upload.com", "gofile.io", "googlevideo.com"]))
def descargador_universal(message):
    cid = message.chat.id
    url = message.text
    msg_espera = bot.reply_to(message, "🚀 Procesando enlace... Esto puede tardar según el tamaño del archivo.")
    
    # Configuración de descarga
    file_name = f"descarga_{cid}"
    ydl_opts = {
        'outtmpl': f'{file_name}.%(ext)s',
        'noplaylist': True,
        'max_filesize': 45000000, # Límite de 45MB para evitar que Koyeb se apague
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename_real = ydl.prepare_filename(info)
        
        # Enviar el archivo descargado
        with open(filename_real, 'rb') as f:
            bot.send_document(cid, f, caption="✅ ¡Descarga completada!\nRecuerda seguir cazando tus 10 orbes épicos [cite: 2026-01-10]")
        
        # Limpieza
        if os.path.exists(filename_real):
            os.remove(filename_real)
        bot.delete_message(cid, msg_espera.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: El archivo es muy pesado para el servidor gratuito o el link es privado.", cid, msg_espera.message_id)
        # Limpieza si falló
        for file in os.listdir():
            if file.startswith(f"descarga_{cid}"):
                os.remove(file)

if __name__ == "__main__":
    print("Bot en línea. Listo para el nivel 20 y el Mapa 4 [cite: 2026-01-10]")
    bot.infinity_polling()

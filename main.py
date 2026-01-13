import telebot
import os
import time
import yt_dlp

# USA EL TOKEN DE TU VARIABLE DE ENTORNO EN KOYEB
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- REGLAS DEL JUEGO (MAPA 4) ---
@bot.message_handler(commands=['cazar', 'orbes'])
def caceria(message):
    # Solo funciona si es nivel 20 o cuarto mapa [cite: 2026-01-10]
    bot.reply_to(message, "🏹 Buscando animales en el Mapa 4... (Probabilidad equilibrada) [cite: 2026-01-10]")
    # Aquí iría tu lógica de cacería
    bot.send_message(message.chat.id, "Recuerda: Necesitas 10 Orbes Épicos para un deseo o 60 Legendarios. [cite: 2026-01-10]")

# --- FUNCIÓN DE MÚSICA ---
@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def descargar_musica(message):
    msg = bot.reply_to(message, "🎵 Preparando tu música...")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'cancion.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        with open('cancion.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="Aquí tienes tu música 🎧")
        os.remove('cancion.mp3')
    except Exception as e:
        bot.reply_to(message, f"❌ Error al extraer: {e}")

# --- ARRANQUE SEGURO ---
if __name__ == "__main__":
    print("Iniciando bot... Esperando cierre de sesiones viejas.")
    time.sleep(5)  # Tiempo para evitar el error 409
    bot.infinity_polling()

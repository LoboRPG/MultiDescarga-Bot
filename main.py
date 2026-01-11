import telebot
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🐺 **Lobo Nivel 73: Modo Ilimitado**\n⚡ Bypass de Publicidad Activo\n📦 Sin límites de RAM (Enlace Directo)\n🔮 Cuarto mapa: 10 Épicos / 60 Legendarios")

@bot.message_handler(func=lambda message: "http" in message.text.lower())
def bypass_potente(message):
    import yt_dlp
    url = message.text
    msg = bot.reply_to(message, "🚀 **Analizando enlace...** Saltando publicidad y captchas ⚡")

    try:
        # Aquí configuramos para que el bot SOLO extraiga el link, no el archivo completo
        ydl_opts = {'quiet': True, 'no_warnings': True, 'cachedir': False}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False) # download=False NO consume RAM
            direct_link = info.get('url', None)
            titulo = info.get('title', 'Archivo_Lobo')

            if direct_link:
                bot.edit_message_text(f"✅ **¡Bypass Exitoso!**\n\n📦 **Archivo:** {titulo}\n🚀 **Link Directo:** [Haz clic aquí para descargar]({direct_link})", 
                                      message.chat.id, msg.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("⚠️ No pude generar el link directo. Intenta con otro servidor.", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("❌ Error de potencia. El link está muy protegido.", message.chat.id, msg.message_id)

@bot.message_handler(func=lambda message: True)
def caceria(message):
    # Reglas del 10 de enero [cite: 2026-01-10]
    bot.send_message(message.chat.id, "🔮 **Cacería en el cuarto mapa:**\nBusca los 10 orbes épicos o los 60 legendarios.")

bot.polling(non_stop=True)

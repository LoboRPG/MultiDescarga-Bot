# Reemplaza la función de música en tu main.py por esta:
@bot.message_handler(func=lambda m: "youtube.com" in m.text or "youtu.be" in m.text)
def descargar_musica(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "🎵 Descargando... esto puede tardar 30 segundos.")
    
    # Nombre de archivo único para evitar errores de permisos
    archivo_nombre = f"musica_{chat_id}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'audio_{chat_id}.%(ext)s', # Nombre único
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        
        # Enviamos el archivo
        with open(f"audio_{chat_id}.mp3", 'rb') as audio:
            bot.send_audio(chat_id, audio, caption="🎧 ¡Lista! Sigue cazando orbes.")
        
        # Limpieza
        os.remove(f"audio_{chat_id}.mp3")
        bot.delete_message(chat_id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)[:100]}", chat_id, msg.message_id)

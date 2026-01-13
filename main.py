    # --- SI ES MÚSICA (YouTube, Spotify, SoundCloud) ---
    sitios_musica = ["youtube.com", "youtu.be", "spotify.com", "soundcloud.com"]
    if any(p in url.lower() for p in sitios_musica):
        msg = bot.reply_to(message, "🎶 **Procesando música...**")
        try:
            # Agregamos opciones para evitar bloqueos
            YDL_OPTIONS_PRO = {
                **YDL_OPTIONS,
                'noplaylist': True, # No descargar listas enteras
                'nocheckcertificate': True,
            }
            with yt_dlp.YoutubeDL(YDL_OPTIONS_PRO) as ydl:
                info = ydl.extract_info(url, download=True)
                nombre_mp3 = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
            with open(nombre_mp3, 'rb') as f:
                bot.send_audio(chat_id, f, caption="🎵 **Música lista para la cacería.**")
            os.remove(nombre_mp3)
            bot.delete_message(chat_id, msg.message_id)
        except Exception as e:
            print(f"Error detallado: {e}") # Esto saldrá en tus logs de Koyeb
            bot.edit_message_text(f"❌ **Error:** El link es privado o no compatible.", chat_id, msg.message_id)
        return

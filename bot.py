import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURACIÓN ---
api_id = 35193604 
api_hash = "86ebd1d9bfb9d04ef79fe2a600677f35"
bot_token = "8207131840:AAEurLqsE4k2K4cQynaY_qInvQyZsBhhS3Y" 

# CANALES
canal_boveda = -1003539534578 
canal_publico = -1003480222023 # ID de @MisPeli2026 proporcionado

api_ouo = "s1U3jzcl" 
mi_id = 6261729070 
bot_username = "Upload_X_Telegram_bot" 
pass_archivo = "HonorPro2026"

app = Client("honorpro_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# 1. ENTREGA DE ARCHIVOS (Cuando el usuario toca el botón)
@app.on_message(filters.command("start") & filters.private)
async def entrega_video(client, message):
    if len(message.command) > 1:
        data = message.command[1]
        if data.startswith("peli_"):
            try:
                msg_id = int(data.replace("peli_", ""))
                await message.reply_text(f"🔐 **Contraseña para extraer:** `{pass_archivo}`")
                
                archivo = await client.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=canal_boveda,
                    message_id=msg_id,
                    caption=f"**HonorPro Bot** 🛡️\n\nArchivo listo. Se eliminará en 15 min."
                )
                
                await asyncio.sleep(900)
                await archivo.delete()
            except Exception:
                await message.reply_text("❌ El archivo ya no está disponible.")
    else:
        await message.reply_text("👋 Bienvenido. Busca tus películas en @MisPeli2026")

# 2. PUBLICADOR AUTOMÁTICO AL CANAL (Solo tú)
@app.on_message(filters.command("post") & filters.user(mi_id))
async def publicar_en_canal(client, message):
    # Formato: /post [ID_FOTO] [ID_VIDEO] [Año] [Genero] [Nombre]
    if len(message.command) > 5:
        id_foto = message.command[1]
        id_video = message.command[2]
        year = message.command[3]
        genero = message.command[4]
        nombre = " ".join(message.command[5:])
        
        link_destino = f"https://t.me/{bot_username}?start=peli_{id_video}"
        url_api = f"http://ouo.io/api/{api_ouo}?s={link_destino}"
        
        try:
            res = requests.get(url_api)
            link_final = res.text.strip()
            
            texto_post = (
                f"🎬 **{nombre.upper()}**\n\n"
                f"📅 **Año:** {year}\n"
                f"🎭 **Género:** {genero}\n"
                f"🔐 **Contraseña:** `{pass_archivo}`\n\n"
                f"🚀 _Toca el botón de abajo para ver la película._"
            )
            
            # EL BOT PUBLICA DIRECTAMENTE EN EL CANAL PÚBLICO
            post_canal = await client.copy_message(
                chat_id=canal_publico,
                from_chat_id=canal_boveda,
                message_id=int(id_foto),
                caption=texto_post,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📥 VER PELÍCULA AQUÍ", url=link_final)]
                ])
            )
            
            # Confirmación para ti
            await message.reply_text(
                f"✅ **¡Publicado en el canal!**\n"
                f"🔗 [Ver post en @MisPeli2026](https://t.me/MisPeli2026/{post_canal.id})",
                disable_web_page_preview=True
            )
            
        except Exception as e:
            await message.reply_text(f"❌ Error al publicar: {e}\n\nAsegúrate de que el bot sea Administrador del canal.")
    else:
        await message.reply_text("Usa: `/post [ID_Foto] [ID_Video] [Año] [Género] [Nombre]`")

# 3. CAMBIAR CONTRASEÑA
@app.on_message(filters.command("setpass") & filters.user(mi_id))
async def cambiar_pass(client, message):
    global pass_archivo
    if len(message.command) > 1:
        pass_archivo = message.command[1]
        await message.reply_text(f"✅ Contraseña actualizada: `{pass_archivo}`")

print("🚀 BOT PUBLICADOR ACTIVO - @MisPeli2026")
app.run()
            

import os, asyncio, uuid, re, sys
from telethon import TelegramClient, events, Button
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

# Configuración confirmada
API_ID = 31097867
API_HASH = '09d0de2ae397c7db6a631514a9cd8efb'
BOT_TOKEN = '8486419403:AAGJb4g0oxj82wAzAA-GmZ-ogEBoPhGpD1s'
CANAL_ID = -1003718270063 
ADMIN_ID = 7779201071 

bot = TelegramClient('sesion_final', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
cola_espera = asyncio.Queue()
db_links = {}

@bot.on(events.NewMessage(incoming=True, from_users=ADMIN_ID))
async def updater(event):
    if event.file and event.file.name == 'bot.py':
        await event.reply("📥 **Actualización Anti-Bloqueo recibida.** Reiniciando...")
        await bot.download_media(event.message, 'bot.py')
        os.system("systemctl restart telegram-bot")

async def verificar_suscripcion(user_id):
    try:
        await bot(GetParticipantRequest(CANAL_ID, user_id))
        return True
    except UserNotParticipantError:
        return False
    except Exception:
        return True 

@bot.on(events.NewMessage)
async def handle_msg(event):
    if event.text.startswith('/') or (event.file and event.sender_id == ADMIN_ID): return
    
    tipo = None
    if "instagram.com" in event.text: tipo = "Instagram"
    elif "mediafire.com" in event.text: tipo = "MediaFire"
    
    if not tipo: return
    
    if not await verificar_suscripcion(event.sender_id):
        await event.reply("⚠️ Únete al canal para descargar.", 
            buttons=[[Button.url("📢 Unirme", "https://t.me/Novedades2_Bot")], [Button.inline("🔄 Verificar", "verificar")]])
        return
    
    short_id = str(uuid.uuid4())[:8]
    db_links[short_id] = event.text.strip()
    await event.reply(f"💎 **Link de {tipo} detectado**", 
                     buttons=[[Button.inline(f"✅ Descargar", f"dl_{short_id}")]])

@bot.on(events.CallbackQuery)
async def manager(event):
    data = event.data.decode()
    if data == "verificar":
        if await verificar_suscripcion(event.sender_id): await event.edit("✅ ¡Listo!")
        else: await event.answer("❌ No te has unido.", alert=True)
    elif data.startswith("dl_"):
        url = db_links.get(data.replace("dl_", ""))
        if url:
            msg = await event.edit("⏳ **Bypass de seguridad activado...**")
            await cola_espera.put((url, msg, event.chat_id))

async def trabajador(n):
    while True:
        url, msg, chat_id = await cola_espera.get()
        folder = f"tmp_{uuid.uuid4().hex[:6]}"
        os.makedirs(folder, exist_ok=True)
        
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        
        output_template = os.path.join(folder, "%(title)s.%(ext)s")
        if "instagram.com" in url:
            output_template = os.path.join(folder, "video.mp4")

        try:
            cmd = f'yt-dlp -4 --user-agent "{user_agent}" --no-check-certificate "{url}" -o "{output_template}"'
            process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await process.wait()
            
            archivos = os.listdir(folder)
            if archivos:
                file_path = os.path.join(folder, archivos[0])
                await bot.send_file(chat_id, file_path, caption=f"✅ Video entregado\n\n@Novedades2_Bot")
                await msg.delete()
            else:
                await msg.edit("❌ Error de red. Intentando de nuevo...")
        except: pass
        finally:
            os.system(f"rm -rf {folder}")
            cola_espera.task_done()

async def main():
    for i in range(1, 6):
        bot.loop.create_task(trabajador(i))
    await bot.run_until_disconnected()

if __name__ == '__main__':
    bot.loop.run_until_complete(main())

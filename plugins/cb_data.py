import pyromod.listen

from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os, random, time
from PIL import Image
from helper.ffmpeg import take_screen_shot, fix_thumb, add_metadata
from helper.database import find
from config import *

# ================= USERBOT CLIENT =================

app = Client(
    "RenamerUser",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    plugins=dict(root="plugins")
)

# ================= CANCEL =================

@app.on_callback_query(filters.regex("^cancel$"))
async def cancel(_, update):
    try:
        await update.message.reply_to_message.delete()
    except:
        pass
    try:
        await update.message.delete()
    except:
        pass

# ================= RENAME =================

@app.on_callback_query(filters.regex("^rename$"))
async def rename(_, update):
    msg_id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(
        "Please Enter The New Filename...\n\nNote : Extension Not Required",
        reply_to_message_id=msg_id,
        reply_markup=ForceReply(True)
    )

# ================= DOCUMENT =================

@app.on_callback_query(filters.regex("^doc$"))
async def doc(_, update):

    os.makedirs("Metadata", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

    try:
        new_filename = update.message.text.split(":-", 1)[1]
    except:
        return await update.message.edit("❌ Filename parse error.")

    file_path = f"downloads/{new_filename}"

    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await app.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    data = find(message.chat.id)
    if data[2]:
        await add_metadata(path, f"Metadata/{new_filename}", data[3], ms)

    os.rename(path, file_path)

    thumb, caption = data[:2]
    caption = caption or f"**{new_filename}**"

    ph_path = None
    if thumb:
        ph_path = await app.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path, "JPEG")

    await ms.edit("🚀 Uploading...")
    c_time = time.time()

    await app.send_document(
        update.from_user.id,
        document=file_path,
        thumb=ph_path,
        caption=caption,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Uploading...", ms, c_time)
    )

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)

# ================= VIDEO =================

@app.on_callback_query(filters.regex("^vid$"))
async def vid(_, update):

    os.makedirs("Metadata", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

    try:
        new_filename = update.message.text.split(":-", 1)[1]
    except:
        return await update.message.edit("❌ Filename parse error.")

    file_path = f"downloads/{new_filename}"

    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await app.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    data = find(message.chat.id)
    if data[2]:
        await add_metadata(path, f"Metadata/{new_filename}", data[3], ms)

    os.rename(path, file_path)

    duration = 0
    meta = extractMetadata(createParser(file_path))
    if meta and meta.has("duration"):
        duration = meta.get("duration").seconds

    thumb, caption = data[:2]
    caption = caption or f"**{new_filename}**"

    ph_path = None
    if thumb:
        ph_path = await app.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path, "JPEG")
    else:
        try:
            ss, = await take_screen_shot(
                file_path, ".", random.randint(0, max(duration - 1, 1))
            )
            _, _, ph_path = await fix_thumb(ss)
        except:
            pass

    await ms.edit("🚀 Uploading...")
    c_time = time.time()

    await app.send_video(
        update.from_user.id,
        video=file_path,
        thumb=ph_path,
        duration=duration,
        caption=caption,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Uploading...", ms, c_time)
    )

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)

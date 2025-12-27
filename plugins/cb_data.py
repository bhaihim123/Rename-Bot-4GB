from helper.progress import progress_for_pyrogram, humanbytes
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os, random, time
from PIL import Image
from helper.ffmpeg import take_screen_shot, fix_thumb, add_metadata
from helper.database import find
from config import *

# ===== USERBOT CLIENT (ONLY ONE CLIENT) =====
app = Client(
    "RenamerUser",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# ================== CALLBACKS ==================

@app.on_callback_query(filters.regex("cancel"))
async def cancel(_, query):
    try:
        await query.message.delete()
        await query.message.reply_to_message.delete()
    except:
        await query.message.delete()

@app.on_callback_query(filters.regex("rename"))
async def rename(_, query):
    msg_id = query.message.reply_to_message_id
    await query.message.delete()
    await query.message.reply_text(
        "__Please Enter The New Filename...__\n\n**Note :** Extension Not Required",
        reply_to_message_id=msg_id,
        reply_markup=ForceReply(True)
    )

# ===================== DOCUMENT =====================

@app.on_callback_query(filters.regex("doc"))
async def doc(_, query):

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_filename = query.message.text.split(":-")[1]
    file_path = f"downloads/{new_filename}"

    message = query.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await query.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await app.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    os.rename(path, file_path)

    data = find(int(query.message.chat.id))
    thumb = data[0]
    caption = data[1] or f"**{new_filename}**"

    ph_path = None
    if thumb:
        ph_path = await app.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path, "JPEG")

    await ms.edit("🚀 Uploading...")
    c_time = time.time()

    await app.send_document(
        query.from_user.id,
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

# ===================== VIDEO =====================

@app.on_callback_query(filters.regex("vid"))
async def vid(_, query):

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_filename = query.message.text.split(":-")[1]
    file_path = f"downloads/{new_filename}"

    message = query.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await query.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await app.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    os.rename(path, file_path)

    duration = 0
    meta = extractMetadata(createParser(file_path))
    if meta and meta.has("duration"):
        duration = meta.get("duration").seconds

    data = find(int(query.message.chat.id))
    thumb = data[0]
    caption = data[1] or f"**{new_filename}**"

    try:
        ph_path_, = await take_screen_shot(
            file_path,
            os.path.dirname(os.path.abspath(file_path)),
            random.randint(0, max(duration - 1, 1))
        )
        _, _, ph_path = await fix_thumb(ph_path_)
    except:
        ph_path = None

    await ms.edit("🚀 Uploading...")
    c_time = time.time()

    await app.send_video(
        query.from_user.id,
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

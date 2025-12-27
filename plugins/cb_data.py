from helper.progress import progress_for_pyrogram, humanbytes
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os, random, time
from PIL import Image
from datetime import timedelta
from helper.ffmpeg import take_screen_shot, fix_thumb, add_metadata
from helper.set import escape_invalid_curly_brackets
from helper.database import find
from config import *

# User Client (for 4GB with STRING_SESSION)
app = Client(
    "JishuBotz",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
        await update.message.reply_to_message.delete()
    except:
        await update.message.delete()

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    chat_id = update.message.chat.id
    msg_id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(
        "__Please Enter The New Filename...__\n\n**Note :** Extension Not Required",
        reply_to_message_id=msg_id,
        reply_markup=ForceReply(True)
    )

# ===================== DOCUMENT =====================

@Client.on_callback_query(filters.regex("doc"))
async def doc(bot, update):

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"

    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await bot.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    _bool_metadata = find(int(message.chat.id))[2]
    if _bool_metadata:
        metadata = find(int(message.chat.id))[3]
        metadata_path = f"Metadata/{new_filename}"
        await add_metadata(path, metadata_path, metadata, ms)
    else:
        metadata_path = path

    os.rename(path, file_path)

    data = find(int(update.message.chat.id))
    thumb = data[0]
    caption = data[1] or f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").resize((320, 320)).save(ph_path, "JPEG")
    else:
        ph_path = None

    await ms.edit("🚀 Uploading...")
    c_time = time.time()

    if file.file_size > 2090000000:
        sent = await app.send_document(
            LOG_CHANNEL,
            document=file_path,
            thumb=ph_path,
            caption=caption,
            progress=progress_for_pyrogram,
            progress_args=("🚀 Uploading...", ms, c_time)
        )
        await bot.copy_message(update.from_user.id, sent.chat.id, sent.id)
    else:
        await bot.send_document(
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

# ===================== VIDEO =====================

@Client.on_callback_query(filters.regex("vid"))
async def vid(bot, update):

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"

    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await bot.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    _bool_metadata = find(int(message.chat.id))[2]
    if _bool_metadata:
        metadata = find(int(message.chat.id))[3]
        metadata_path = f"Metadata/{new_filename}"
        await add_metadata(path, metadata_path, metadata, ms)
    else:
        metadata_path = path

    os.rename(path, file_path)

    duration = 0
    meta = extractMetadata(createParser(file_path))
    if meta and meta.has("duration"):
        duration = meta.get("duration").seconds

    data = find(int(update.message.chat.id))
    thumb = data[0]
    caption = data[1] or f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").resize((320, 320)).save(ph_path, "JPEG")
    else:
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

    if file.file_size > 2090000000:
        sent = await app.send_video(
            LOG_CHANNEL,
            video=file_path,
            thumb=ph_path,
            duration=duration,
            caption=caption,
            progress=progress_for_pyrogram,
            progress_args=("🚀 Uploading...", ms, c_time)
        )
        await bot.copy_message(update.from_user.id, sent.chat.id, sent.id)
    else:
        await bot.send_video(
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

# ===================== AUDIO =====================

@Client.on_callback_query(filters.regex("aud"))
async def aud(bot, update):

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{new_filename}"

    message = update.message.reply_to_message
    file = message.document or message.video or message.audio

    ms = await update.message.edit("🚀 Downloading...")
    c_time = time.time()

    path = await bot.download_media(
        message=file,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Downloading...", ms, c_time)
    )

    os.rename(path, file_path)

    duration = 0
    meta = extractMetadata(createParser(file_path))
    if meta and meta.has("duration"):
        duration = meta.get("duration").seconds

    data = find(int(update.message.chat.id))
    thumb = data[0]
    caption = data[1] or f"**{new_filename}**"

    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").resize((320, 320)).save(ph_path, "JPEG")
    else:
        ph_path = None

    await ms.edit("🚀 Uploading...")
    c_time = time.time()

    await bot.send_audio(
        update.from_user.id,
        audio=file_path,
        caption=caption,
        thumb=ph_path,
        duration=duration,
        progress=progress_for_pyrogram,
        progress_args=("🚀 Uploading...", ms, c_time)
    )

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)

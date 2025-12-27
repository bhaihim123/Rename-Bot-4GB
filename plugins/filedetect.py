from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(
    (filters.private | filters.me) &
    (filters.document | filters.video | filters.audio)
)
async def file_detect(client, message):

    file = message.document or message.video or message.audio
    if not file:
        return

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✏ Rename", callback_data="rename")],
        [
            InlineKeyboardButton("📄 Document", callback_data="doc"),
            InlineKeyboardButton("🎬 Video", callback_data="vid"),
            InlineKeyboardButton("🎵 Audio", callback_data="aud"),
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
    ])

    await message.reply_text(
        "**What Do You Want Me To Do With This File ?**\n\n"
        f"**File Name :** `{file.file_name}`\n"
        f"**File Size :** `{round(file.file_size / (1024*1024), 2)} MB`",
        reply_markup=buttons,
        quote=True
    )

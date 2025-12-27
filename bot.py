import pyromod.listen  # 🔥 MUST (না দিলে listener error আসবে)
import pyrogram.utils
from pyrogram import idle

from plugins.cb_data import app

# Telegram ID limit fix (safe)
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

print("✅ Renamer Userbot Started")

app.start()
idle()
app.stop()

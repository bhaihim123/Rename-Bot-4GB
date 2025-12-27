from plugins.cb_data import app
from pyrogram import idle
import pyrogram.utils

# Telegram ID limit fix (optional but safe)
pyrogram.utils.MIN_CHAT_ID = -999999999999
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999

print("✅ Renamer Userbot Started")

app.start()
idle()
app.stop()

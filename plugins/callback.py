from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from plugins.cb_data import app   # 🔥 সবচেয়ে গুরুত্বপূর্ণ লাইন
from script import *
from config import *


@app.on_callback_query(filters.regex('about'))
async def about(_, update):
    text = script.ABOUT_TXT.format(update.from_user.mention)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="home")]
    ])
    await update.message.edit(text=text, reply_markup=keyboard)


@app.on_message(filters.private & filters.command(["donate"]))
async def donatecm(_, message):
    text = script.DONATE_TXT
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🦋 Admin", url="https://t.me/CallAdminRobot"),
            InlineKeyboardButton("✖️ Close", callback_data="cancel")
        ]
    ])
    await message.reply_text(text=text, reply_markup=keyboard, quote=True)


@app.on_message(filters.private & filters.user(ADMIN) & filters.command(["admin"]))
async def admincm(_, message):
    text = script.ADMIN_TXT
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✖️ Close ✖️", callback_data="cancel")]
    ])
    await message.reply_text(text=text, reply_markup=keyboard, quote=True)


@app.on_callback_query(filters.regex('help'))
async def help_cb(_, update):
    text = script.HELP_TXT.format(update.from_user.mention)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('🏞 Thumbnail', callback_data='thumbnail'),
            InlineKeyboardButton('✏ Caption', callback_data='caption')
        ],
        [
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('💵 Donate', callback_data='donate')
        ]
    ])
    await update.message.edit(text=text, reply_markup=keyboard)


@app.on_callback_query(filters.regex('thumbnail'))
async def thumbnail(_, update):
    text = script.THUMBNAIL_TXT
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="help")]
    ])
    await update.message.edit(text=text, reply_markup=keyboard)


@app.on_callback_query(filters.regex('caption'))
async def caption(_, update):
    text = script.CAPTION_TXT
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="help")]
    ])
    await update.message.edit(text=text, reply_markup=keyboard)


@app.on_callback_query(filters.regex('donate'))
async def donate(_, update):
    text = script.DONATE_TXT
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="help")]
    ])
    await update.message.edit(text=text, reply_markup=keyboard)


@app.on_callback_query(filters.regex('home'))
async def home_callback_handler(_, query):
    text = (
        f"Hello {query.from_user.mention}\n\n"
        "➻ This Is An Advanced And Yet Powerful Rename Bot.\n\n"
        "➻ Using This Bot You Can Rename And Change Thumbnail Of Your Files.\n\n"
        "➻ You Can Also Convert Video To File And File To Video.\n\n"
        "➻ This Bot Also Supports Custom Thumbnail And Custom Caption.\n\n"
        "<b>Bot Is Made By @Madflix_Bots</b>"
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📢 Updates", url="https://t.me/Madflix_Bots"),
            InlineKeyboardButton("💬 Support", url="https://t.me/MadflixBots_Support")
        ],
        [
            InlineKeyboardButton("🛠️ Help", callback_data='help'),
            InlineKeyboardButton("❤️‍🩹 About", callback_data='about')
        ],
        [
            InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/CallAdminRobot")
        ]
    ])
    await query.message.edit_text(text=text, reply_markup=keyboard)

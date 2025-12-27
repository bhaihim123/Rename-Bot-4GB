from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import find_one
from helper.progress import humanbytes


@Client.on_message(filters.private & filters.command(["myplan"]))
async def myplan(client, message):

    user_id = message.from_user.id
    data = find_one(user_id)

    # FORCE UNLIMITED VALUES
    used = 0
    limit = 10**18
    remain = limit
    user = "Unlimited"

    text = (
        f"<b>User ID :</b> <code>{user_id}</code>\n"
        f"<b>Name :</b> {message.from_user.mention}\n\n"
        f"<b>🏷 Plan :</b> {user}\n\n"
        f"✓ Upload Size : Unlimited\n"
        f"✓ Daily Upload : Unlimited\n"
        f"✓ Today Used : Unlimited\n"
        f"✓ Remain : Unlimited\n"
        f"✓ Timeout : 0 Second\n"
        f"✓ Parallel Process : Unlimited\n"
        f"✓ Time Gap : No\n\n"
        f"<b>Validity :</b> Lifetime"
    )

    await message.reply(
        text,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖️ Close", callback_data="cancel")]]
        )
    )

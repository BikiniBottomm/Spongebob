from pyrogram import filters
from Spongebob.modules.helper_funcs.pbot import list_admins
from Spongebob import pbot as spopy

@spopy.on_message(
    filters.command(["report", "admins"], prefixes=["@", "/"])
    & ~filters.edited
)

async def report_user(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply a message from user to report him ")
    list_of_admins = await list_admins(message.chat.id)
    user_mention = message.reply_to_message.from_user.mention
    text = f"Reported {user_mention}!."
    for admin in list_of_admins:
        text += f"[\u2063](tg://user?id={admin})"
    await message.reply_text(text)

from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import ChatPermissions, Message
from pyrogram.errors import BadRequest
import aiohttp, json, asyncio

from Spongebob import pbot, CF_API_KEY, EVENT_LOGS
import Spongebob.modules.sql.nsfw_sql as sql

from pyrogram.types import Message

session = aiohttp.ClientSession()


async def admin_check(message: Message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    return check_status.status in admin_strings


@pbot.on_message(filters.command("nsfwdetect"), group=8)
async def nsfw_detect(client, message):
    is_admin = await admin_check(message)
    args = message.text.split(None, 1)

    if is_admin == True:
        if len(args) > 1:
            if args[1].lower() in ["on", "yes"]:
                sql.enable_nsfw(message.chat.id)
                await message.reply_text(
                    "I've enabled Nsfw Protection moderation in this group. This will help protect you "
                    "from nsfw content."
                )
            elif args[1].lower() in ["off", "no"]:
                sql.disable_nsfw(message.chat.id)
                await message.reply_text(
                    "I've disabled Nsfw Protection moderation in this group. Nsfw can detected in this group "
                    "anymore. You'll be less protected from any nsfw contect "
                    "though!"
                )
        else:
            await message.reply_text(
                "Give me some arguments to choose a setting! on/off, yes/no!\n\n"
                "Your current setting is: {}\n"
                "When True, any messsages will go through NLP and spammers will be banned.\n"
                "When False, they won't, leaving you at the possible mercy of spammers\n"
                "Nsfw powered by @Intellivoid.".format(sql.does_chat_nlp(message.chat.id))
            )
    else:
        await message.reply_text("You not an admin.")
        
@pbot.on_message(filters.photo & filters.group, group=3)
async def detecting_nsfw(client, message):
    url = "https://api.intellivoid.net/coffeehouse/v1/image/nsfw_classification"
    user = message.from_user
    chat = message.chat
    msg = message.text
    chat_state = sql.does_chat_nsfw(chat.id)
    if CF_API_KEY and chat_state == True:
        try:
            payload = {'access_key': CF_API_KEY, 'input': msg}
            data = await session.post(url, data=payload)
            res_json = await data.json()
            if res_json['success']:
                nsfw_checking = res_json['results']['nsfw_classification']['is_nsfw']
                if nsfw_checking == True:
                    pred = res_json['results']['nsfw_classification']['content_type']
                    sepi = res_json['results']['nsfw_classification']['safe_prediction']
                    predic = res_json['results']['nsfw_classification']['unsafe_prediction']
                    await pbot.restrict_chat_member(chat.id, user.id, ChatPermissions(can_send_media=False))
                    try:
                        await message.reply_text(
                        f"**⚠ NSFW DETECTED!**\nContent Type: `{pred}`\nSafe prediction: `{sepi}` Unsafe prediction: `{predic}` User: `{user.id}` was muted.",
                        parse_mode="md",
                    )
                    except BadRequest:
                        await message.reply_text(
                        f"**⚠ NSFW DETECTED!**\nContent Type: `{pred}`\nSafe prediction: `{sepi}` Unsafe prediction: `{predic}` User: `{user.id}`\nnUser could not be restricted due to insufficient admin perms.",
                        parse_mode="md",
                    )

            elif res_json['error']['error_code'] == 21:
                reduced_msg = msg[0:170]
                payload = {'access_key': CF_API_KEY, 'input': reduced_msg}
                data = await session.post(url, data=payload)
                res_json = await data.json()
                spam_check = res_json['results']['nsfw_classification']['is_nsfw']
                if spam_check is True:
                    pred = res_json['results']['nsfw_classification']['content_type']
                    await pbot.restrict_chat_member(chat.id, user.id, ChatPermissions(can_send_media=False))
                    try:
                        await message.reply_text(
                            f"**⚠ NSFW DETECT!**\nContent type: `{pred}`\nUser: `{user.id}` was muted.", parse_mode="markdown")
                    except BadRequest:
                        await message.reply_text(f"**⚠ NSFW DETECTED!**\nContent type: `{pred}`\nUser: `{user.id}`\nUser could not be restricted due to insufficient admin perms.", parse_mode="markdown")
        except (aiohttp.ClientConnectionError, asyncio.TimeoutError):
            log.warning("Can't reach SpamProtection API")
            await asyncio.sleep(0.5)
            
            
@pbot.on_message(filters.animation & filters.group, group=3)
async def detecting_nsfw(client, message):
    url = "https://api.intellivoid.net/coffeehouse/v1/image/nsfw_classification"
    user = message.from_user
    chat = message.chat
    msg = message.text
    chat_state = sql.does_chat_nsfw(chat.id)
    if CF_API_KEY and chat_state == True:
        try:
            payload = {'access_key': CF_API_KEY, 'input': msg}
            data = await session.post(url, data=payload)
            res_json = await data.json()
            if res_json['success']:
                nsfw_checking = res_json['results']['nsfw_classification']['is_nsfw']
                if nsfw_checking == True:
                    pred = res_json['results']['nsfw_classification']['content_type']
                    sepi = res_json['results']['nsfw_classification']['safe_prediction']
                    predic = res_json['results']['nsfw_classification']['unsafe_prediction']
                    await pbot.restrict_chat_member(chat.id, user.id, ChatPermissions(can_send_media=False))
                    try:
                        await message.reply_text(
                        f"**⚠ NSFW DETECTED!**\nContent Type: `{pred}`\nSafe prediction: `{sepi}` Unsafe prediction: `{predic}` User: `{user.id}` was muted.",
                        parse_mode="md",
                    )
                    except BadRequest:
                        await message.reply_text(
                        f"**⚠ NSFW DETECTED!**\nContent Type: `{pred}`\nSafe prediction: `{sepi}` Unsafe prediction: `{predic}` User: `{user.id}`\nnUser could not be restricted due to insufficient admin perms.",
                        parse_mode="md",
                    )

            elif res_json['error']['error_code'] == 21:
                reduced_msg = msg[0:170]
                payload = {'access_key': CF_API_KEY, 'input': reduced_msg}
                data = await session.post(url, data=payload)
                res_json = await data.json()
                spam_check = res_json['results']['nsfw_classification']['is_nsfw']
                if spam_check is True:
                    pred = res_json['results']['nsfw_classification']['content_type']
                    await pbot.restrict_chat_member(chat.id, user.id, ChatPermissions(can_send_media=False))
                    try:
                        await message.reply_text(
                            f"**⚠ NSFW DETECT!**\nContent type: `{pred}`\nUser: `{user.id}` was muted.", parse_mode="markdown")
                    except BadRequest:
                        await message.reply_text(f"**⚠ NSFW DETECTED!**\nContent type: `{pred}`\nUser: `{user.id}`\nUser could not be restricted due to insufficient admin perms.", parse_mode="markdown")
        except (aiohttp.ClientConnectionError, asyncio.TimeoutError):
            log.warning("Can't reach SpamProtection API")
            await asyncio.sleep(0.5)
                

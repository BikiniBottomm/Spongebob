from pyrogram.types import ChatPermissions, Message
from Spongebob import pbot as spo

async def list_admins(chat_id: int):
    list_of_admins = []
    async for member in spo.iter_chat_members(
        chat_id, filter="administrators"
    ):
        list_of_admins.append(member.user.id)
    return list_of_admins


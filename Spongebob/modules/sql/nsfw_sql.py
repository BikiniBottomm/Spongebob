import threading

from sqlalchemy import Column, UnicodeText, Integer, String, Boolean

from Spongebob.modules.sql import BASE, SESSION



class NSFWSettings(BASE):
    __tablename__ = "chat_nsfw_settings"
    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=False, nullable=False)

    def __init__(self, chat_id, disabled):
        self.chat_id = str(chat_id)
        self.setting = disabled

    def __repr__(self):
        return "<NSFW setting {} ({})>".format(self.chat_id, self.setting)


NSFWSettings.__table__.create(checkfirst=True)

NSFW_SETTING_LOCK = threading.RLock()
NSFW_LIST = set()


def enable_nsfw(chat_id):
    with NSFW_SETTING_LOCK:
        chat = SESSION.query(NSFWSettings).get(str(chat_id))
        if not chat:
            chat = NSFWSettings(chat_id, True)

        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()
        if str(chat_id) in NSFW_LIST:
            NSFW_LIST.remove(str(chat_id))


def disable_nsfw(chat_id):
    with NSFW_SETTING_LOCK:
        chat = SESSION.query(NSFWSettings).get(str(chat_id))
        if not chat:
            chat = NSFWSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()
        nsfw_LIST.add(str(chat_id))


def does_chat_nsfw(chat_id):
    return str(chat_id) not in NSFW_LIST



def __load_nsfw_stat_list():
    global NSFW_LIST
    try:
        NSFW_LIST = {
            x.chat_id for x in SESSION.query(NSFWSettings).all() if not x.setting
        }
    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with NSFW_SETTING_LOCK:
        chat = SESSION.query(NSFWSettings).get(str(old_chat_id))
        if chat:
            chat.chat_id = new_chat_id
            SESSION.add(chat)

        SESSION.commit()


# Create in memory userid to avoid disk access
__load_nsfw_stat_list()

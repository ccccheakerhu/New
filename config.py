
import json
from telegram import Bot

ADMIN_ID = 8020848509
CHANNEL_ID = "@Ghost_Carderr"
DATABASE_FILE = "database.json"

def load_database():
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}, "codes": {}, "groups": {}}

def save_database():
    with open(DATABASE_FILE, "w") as f:
        json.dump(database, f, indent=2)

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id='@Ghost_Carderr', user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

database = load_database()

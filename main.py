import json
import logging
import os
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set your bot token and admin details directly here
BOT_TOKEN = "8430527380:AAEPuPvnglL962Ff4UgMXUEFbCyLYh62Tgw"
ADMIN_ID = 8020848509
CHANNEL_ID = "@Ghost_Carderr"

# Sample in-memory database
database = {
    "users": {},
    "codes": {}
}

def save_database():
    with open("database.json", "w") as f:
        json.dump(database, f)

def check_subscription(bot, user_id):
    # Dummy implementation (should be replaced with real check)
    return True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    if str(user_id) not in database["users"]:
        database["users"][str(user_id)] = {"premium": None, "username": username}
        save_database()

    if not await check_subscription(context.bot, user_id):
        await update.message.reply_text("❌ Please join our channel to use this bot: https://t.me/+mSXYiBgDsXZhNTdl")
        return

    await update.message.reply_text(f"👋 Hello {update.effective_user.first_name} (@{username})! Welcome to the bot.")

async def generate_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return
    try:
        days = int(context.args[0])
        code = f"CODE{len(database['codes'])+1}"
        expiry = (datetime.utcnow() + timedelta(days=days)).strftime("%Y-%m-%d")
        database["codes"][code] = expiry
        save_database()
        await update.message.reply_text(f"✅ Code generated: `{code}` (Valid till {expiry})", parse_mode="Markdown")
    except:
        await update.message.reply_text("Usage: /generatecode <days>")

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    try:
        code = context.args[0]
        if code not in database["codes"]:
            await update.message.reply_text("❌ Invalid code.")
            return
        expiry = database["codes"].pop(code)
        database["users"][user_id]["premium"] = expiry
        save_database()
        await update.message.reply_text(f"✅ Premium activated till {expiry}")
    except:
        await update.message.reply_text("Usage: /redeem <code>")

async def mass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in database["users"] or not database["users"][user_id]["premium"]:
        await update.message.reply_text("❌ Premium required. Contact @Ghost_Carderr.")
        return
    await update.message.reply_text("🧪 Mass check started (demo response).")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generatecode", generate_code))
    app.add_handler(CommandHandler("redeem", redeem))
    app.add_handler(CommandHandler("mass", mass))

    app.run_polling()

if __name__ == "__main__":
    main()

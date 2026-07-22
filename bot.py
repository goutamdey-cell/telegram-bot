from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = "8995087250:AAHhoO1OViO6sryyi-dOHUNjOXqVQOBpy6I"
OWNER_ID = 7504827194

CHANNELS = {
    "Channel 1": -1002310611158,
    "Channel 2": -1002363675161,
    "Channel 3": -1003031914625,
    "Channel 4": -1002286595341,
    "Channel 5": -1003468908725,
    "Channel 6": -1003589730154,
    "Channel 7": -1003861000989,
    "Channel 8": -1003587390302,
    "Channel 9": -1003833989680,
    "Channel 10": -1003596567961,
    "Channel 11": -1003944523544,
}

async def only_owner(update: Update):
    return update.effective_user and update.effective_user.id == OWNER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await only_owner(update):
        return
    await update.message.reply_text(
        "Commands:\n/check USER_ID\n/remove USER_ID"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await only_owner(update):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /check USER_ID")
        return

    uid = int(context.args[0])
    found = []

    for name, chat_id in CHANNELS.items():
        try:
            member = await context.bot.get_chat_member(chat_id, uid)
            if member.status not in ("left", "kicked"):
                found.append(name)
        except:
            pass

    if found:
        await update.message.reply_text("User found in:\n" + "\n".join(found))
    else:
        await update.message.reply_text("User not found.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await only_owner(update):
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remove USER_ID")
        return

    uid = int(context.args[0])
    removed = []

    for name, chat_id in CHANNELS.items():
        try:
            await context.bot.ban_chat_member(chat_id, uid)
            await context.bot.unban_chat_member(chat_id, uid, only_if_banned=True)
            removed.append(name)
        except BadRequest:
            pass
        except:
            pass

    if removed:
        await update.message.reply_text("Removed from:\n" + "\n".join(removed))
    else:
        await update.message.reply_text("Nothing removed.")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("remove", remove))

print("Bot Started...")
app.run_polling()

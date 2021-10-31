from bot import AI, LOGGER, dispatcher
from bot.modules.sql import sql as sq
from telegram.ext import CommandHandler
from telegram import ParseMode

# /lorem
def lorem(update, context):
    args = context.args 
    db_response = sq.DB_Updater(update)

    update.effective_message.reply_text(
        AI["Text"]["LOREM"],
        parse_mode=ParseMode.HTML,
    )


# /whatislorem
def wlorem(update, context):
    args = context.args 
    db_response = sq.DB_Updater(update)

    update.effective_message.reply_text(
        AI["Text"]["WLOREM"],
        parse_mode=ParseMode.HTML,
    )

__help__ = """
 - /lorem <text>: Get Lorem text.
 - /whatislorem <reason>: Know About Lorem Text.
"""

__mod_name__ = "LOREM"

lorem_handler = CommandHandler("lorem", lorem)
whatislorem_handler = CommandHandler("whatislorem",wlorem)
dispatcher.add_handler(whatislorem_handler)
dispatcher.add_handler(lorem_handler)

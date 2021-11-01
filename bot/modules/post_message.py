from bot import AI, LOGGER, dispatcher
from bot.modules.sql import sql as sq
from telegram.ext import CommandHandler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup


# /post_message
def post_message(update, context):
    args = context.args
    chat = update.effective_chat
    db_response = sq.DB_Updater(update)
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text("Contact me in PM to get the Options To Post messages.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           context.bot.username))]]))
        return
    else:
        groups = sq.fetch_groups_allowed(update)




__help__ = """
 - /post_msg <feature>: Post a Single Message in Multiple Groups.
"""

__mod_name__ = "Post Message"

post_handler = CommandHandler("post_msg", post_message)
dispatcher.add_handler(post_handler)

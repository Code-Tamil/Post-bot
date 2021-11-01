# import all Modules
from sys import argv
import time
import importlib
import re
import datetime
from typing import List, Dict
import sqlalchemy as db
# Telegram Modules
from telegram import Update, Bot
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler, CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.utils.helpers import escape_markdown
# Import Bot Modules
from bot import LOGGER, START_TIME, TOKEN, updater, dispatcher, AI
from bot.modules import ALL_MODULES
from bot.modules.sql import sql as sq


HELPABLE = {}
IMPORTED = {}

# Importing Details From Modules
for module_name in ALL_MODULES:
    imported_module = importlib.import_module("bot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    
# Readable times
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


# /start 
def start(update:Update, context:CallbackContext):
    args = context.args 
    db_response = sq.DB_Updater(update, context)

    if update.effective_chat.type == "private":
            if args:
                if args[0].lower() == "help":
                    send_help(update.effective_chat.id, AI["Text"]["HELP"])
                    return 0

    update.effective_message.reply_photo(
        AI["Images"]["START_IMAGE"],    
        AI["Text"]["START"].format(
            escape_markdown(str(update.effective_user.first_name)), escape_markdown(str(db_response)),
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
                    [
                        
                        [
                            InlineKeyboardButton(
                                text="🗄 Source code",
                                url="https://github.com/Code-Tamil/Post-bot",
                            ),
                        ],

                        [
                            InlineKeyboardButton(
                                text="🚑 Join US",
                                url="https://linktr.ee/codetamil",
                            ),
                            InlineKeyboardButton(
                                text="🔔 CodeTamil",
                                url="https://t.me/code_tamil",
                            ),
                        ],


                        [
                            InlineKeyboardButton(
                                text="🃏 Discussion Group",
                                url="https://t.me/code_tamilgrp",
                            ),
                        ],

                    ],
                ),
    )



# /help
def help(update:Update, context:CallbackContext):
    args = context.args 
    uptime = get_readable_time(time.time() - START_TIME)
    db_response = sq.DB_Updater(update, context)

    update.effective_message.reply_photo(
        AI["Images"]["HELP_IMAGE"],
        AI["Text"]["HELP"].format(
            escape_markdown(update.effective_user.first_name), escape_markdown(context.bot.first_name),
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

# Help With UI buttons
def get_help(update:Update, context:CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)
    uptime = get_readable_time(time.time() - START_TIME)
    db_response = sq.DB_Updater(update, context)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text("Contact me in PM to get the list of possible commands.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           context.bot.username))]]))
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "Here is the available help for the *{}* module:\n".format(HELPABLE[module].__mod_name__) \
               + HELPABLE[module].__help__
        send_help(chat.id, text, InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

    else:
        send_help(chat.id, AI["Text"]["HELP"])

# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(chat_id=chat_id,
                                text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard)

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

# Paginate the Help Commands
def paginate_modules(page_n: int, module_dict: Dict, prefix, chat=None) -> List:
    if not chat:
        modules = sorted(
            [EqInlineKeyboardButton(x.__mod_name__,
                                    callback_data="{}_module({})".format(prefix, x.__mod_name__.lower())) for x
             in module_dict.values()])
    else:
        modules = sorted(
            [EqInlineKeyboardButton(x.__mod_name__,
                                    callback_data="{}_module({},{})".format(prefix, chat, x.__mod_name__.lower())) for x
             in module_dict.values()])

    pairs = [
    modules[i * 3:(i + 1) * 3] for i in range((len(modules) + 3 - 1) // 3)
    ]



    round_num = len(modules) / 3
    calc = len(modules) - round(round_num)
    if calc == 1:
        pairs.append((modules[-1], ))
    elif calc == 2:
        pairs.append((modules[-1], ))

    return pairs

# Help Buttons
def help_button(bot: Bot, update: Update):
    query = bot.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            text = "Here is the help for the *{}* module:\n".format(HELPABLE[module].__mod_name__) \
                   + HELPABLE[module].__help__
            query.message.edit_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="Back", callback_data="help_back")]]))

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(curr_page - 1, HELPABLE, "help")))

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(HELP_STRINGS,
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, HELPABLE, "help")))

        elif back_match:
            query.message.edit_text(text=AI["Text"]["HELP"],
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")))
        update.bot.answer_callback_query(query.id)

    except BadRequest as excp:
            if excp.message not in [
                'Message is not modified',
                'Query_id_invalid',
                "Message can't be deleted",
            ]:
                LOGGER.exception('Exception in help buttons. %s', str(query.data))


# /about
def about(update, context):
    args = context.args 
    uptime = get_readable_time(time.time() - START_TIME)
    db_response = sq.DB_Updater(update, context)

    update.effective_message.reply_photo(
        AI["Images"]["ABOUT_IMAGE"],
        AI["Text"]["ABOUT"].format(
            escape_markdown(update.effective_user.first_name),escape_markdown(str(update.effective_user.id)),
        ),
        parse_mode=ParseMode.HTML,
    )

# /source 
def source(update:Update, context:CallbackContext):
    args = context.args 
    db_response = sq.DB_Updater(update, context)

    update.effective_message.reply_photo(
        AI["Images"]["SOURCE_IMAGE"],    
        AI["Text"]["SOURCE"].format(
            escape_markdown(str(update.effective_user.first_name)),
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
                    [
                        
                        [
                            InlineKeyboardButton(
                                text="🗄 Source code",
                                url="https://github.com/Code-Tamil/Post-bot",
                            ),
                        ],

                        [
                            InlineKeyboardButton(
                                text="🚑 Join US",
                                url="https://linktr.ee/codetamil",
                            ),
                            InlineKeyboardButton(
                                text="🔔 CodeTamil",
                                url="https://t.me/code_tamil",
                            ),
                        ],


                        [
                            InlineKeyboardButton(
                                text="🃏 Discussion Group",
                                url="https://t.me/code_tamilgrp",
                            ),
                        ],

                    ],
                ),
    )

# /addgrp 
def addgrp(update:Update, context:CallbackContext):
    args = context.args 
    db_response = sq.DB_Updater(update, context)

    update.effective_message.reply_photo(
        AI["Images"]["SOURCE_IMAGE"],    
        AI["Text"]["SOURCE"].format(
            escape_markdown(str(update.effective_user.first_name)),
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
                    [
                        
                        [
                            InlineKeyboardButton(
                                text="☑️ Add me",
                                url="t.me/{}?startgroup=true".format(
                                    context.bot.username,
                                    ),
                                ),
                        ],


                    ],
                ),
    )

# Main Function to run The Bot
def main():
    # handlers
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    about_handler = CommandHandler("about", about)
    source_handler = CommandHandler("source", source)
    add_handler = CommandHandler("addgrp", addgrp)
    #dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(source_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(add_handler)
    # starting
    LOGGER.info("Bot has successfully started")
    updater.start_polling(timeout=15, read_latency=4)
    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Everything is working good!")
    main()

# import all Modules
from sys import argv
import time
import datetime
import sqlalchemy as db
import json
# Telegram Modules
from telegram import Update
from telegram import InlineKeyboardButton
from telegram.ext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.parsemode import ParseMode
from telegram.utils.helpers import escape_markdown
# Import Bot Modules
from bot import LOGGER, START_TIME, TOKEN, updater, dispatcher
from bot.modules.sql import sql as sq

# Texts to be Messages and Images were Loading
with open('text.json') as f:
  AI = json.load(f)


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
    db_response = sq.DB_Updater(update)

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
    db_response = sq.DB_Updater(update)

    update.effective_message.reply_photo(
        AI["Images"]["HELP_IMAGE"],
        AI["Text"]["HELP"].format(
            escape_markdown(update.effective_user.first_name), escape_markdown(context.bot.first_name),
        ),
        parse_mode=ParseMode.MARKDOWN,
    )

# /about
def about(update, context):
    args = context.args 
    uptime = get_readable_time(time.time() - START_TIME)
    db_response = sq.DB_Updater(update)

    update.effective_message.reply_photo(
        AI["Images"]["ABOUT_IMAGE"],
        AI["Text"]["ABOUT"].format(
            escape_markdown(update.effective_user.first_name),escape_markdown(str(update.effective_user.id)),
        ),
        parse_mode=ParseMode.HTML,
    )

# /lorem
def lorem(update, context):
    args = context.args 
    uptime = get_readable_time(time.time() - START_TIME)
    db_response = sq.DB_Updater(update)

    update.effective_message.reply_text(
        AI["Text"]["LOREM"],
        parse_mode=ParseMode.HTML,
    )


# /whatislorem
def wlorem(update, context):
    args = context.args 
    uptime = get_readable_time(time.time() - START_TIME)
    db_response = sq.DB_Updater(update)

    update.effective_message.reply_text(
        AI["Text"]["WLOREM"],
        parse_mode=ParseMode.HTML,
    )


# /source 
def source(update:Update, context:CallbackContext):
    args = context.args 
    db_response = sq.DB_Updater(update)

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
    db_response = sq.DB_Updater(update)

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
    help_handler = CommandHandler("help", help)
    about_handler = CommandHandler("about", about)
    lorem_handler = CommandHandler("lorem", lorem)
    source_handler = CommandHandler("source", source)
    add_handler = CommandHandler("addgrp", addgrp)
    whatislorem_handler = CommandHandler("whatislorem",wlorem)
    #dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(lorem_handler)
    dispatcher.add_handler(source_handler)
    dispatcher.add_handler(add_handler)
    dispatcher.add_handler(whatislorem_handler)
    # starting
    LOGGER.info("Bot has successfully started")
    updater.start_polling(timeout=15, read_latency=4)
    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Everything is working good!")
    main()

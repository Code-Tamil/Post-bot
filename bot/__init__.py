# Importing Modules
import logging
import os
import time
import sys
from dotenv import load_dotenv
import telegram.ext as tg

#setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

#check python version
if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    LOGGER.error(
        "Hello dear, you mush have python version of at least 3.9! So go install the new version."
    )

START_TIME = time.time()

#fetch env things
load_dotenv()
TOKEN = os.environ.get('TOKEN', None)
DB_URI = 'sqlite:///data.db'

#updater and dispatcher
updater = tg.Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

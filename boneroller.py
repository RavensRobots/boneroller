import logging
from telegram.ext import PicklePersistence, Updater

import commands
from bot_token import TOKEN

logging.basicConfig(filename="base.log", level=logging.INFO, datefmt="%m.%d.%y - %H:%M:%S",
                    format="%(levelname)-7s - %(module)-15s - %(asctime)s - %(message)s")

persistence = PicklePersistence(filename="bot_data/boneroller", single_file=False)
updater = Updater(token=TOKEN, use_context=True, persistence=persistence)
dispatcher = updater.dispatcher

commands.init_handlers(dispatcher)
logging.info("Запускаюсь")
updater.start_polling()
updater.idle()

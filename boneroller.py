from telegram.ext import PicklePersistence, Updater

import commands
from bot_token import TOKEN

persistence = PicklePersistence(filename="bot_data/boneroller", single_file=False)
updater = Updater(token=TOKEN, use_context=True, persistence=persistence)
dispatcher = updater.dispatcher

commands.init_handlers(dispatcher)
updater.start_polling()

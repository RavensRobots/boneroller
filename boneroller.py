from telegram.ext import CommandHandler, PicklePersistence, Updater

import manager
from bot_token import TOKEN


persistence = PicklePersistence(filename="bot_data/boneroller", single_file=False)
updater = Updater(token=TOKEN, use_context=True, persistence=persistence)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.greet())


def d6(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.roll_a_dice(6))


def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.get_error_message())


dispatcher.add_handler(CommandHandler('d6', d6))
dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_error_handler(error)

updater.start_polling()

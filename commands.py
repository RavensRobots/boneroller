from telegram.ext import CommandHandler

import manager


def init_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_error_handler(error)

    dispatcher.add_handler(CommandHandler('d6', d6))
    dispatcher.add_handler(CommandHandler('pig', pig))


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.greet())


def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.get_error_message())


def d6(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.roll_a_dice(6))


def pig(update, context):
    pass

from telegram.ext import CommandHandler, Updater
from bot_token import TOKEN
import manager


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.greet())


def bone6(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.roll_a_dice(6))


d6_handler = CommandHandler('d6', bone6)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(d6_handler)
dispatcher.add_handler(start_handler)
updater.start_polling()

import message_parser
import texter
from telegram.ext import CommandHandler, Updater
from bot_token import TOKEN

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет")


def lang(update, context):

    command, message = message_parser.cut_off_command(update.effective_message.text)
    texter.texter.add_users(update.effective_message.from_user.id, message)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Мы добавили локализацию " + message +
                             " для пользователя " + str(update.effective_message.from_user.id))


start_handler = CommandHandler('start', start)
lang_handler = CommandHandler('lang', lang)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(lang_handler)
updater.start_polling()

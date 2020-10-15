import logging
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler

import interface_layout as il
from localization import ul


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков команд")
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('credits', credits_handler))


def start(update, context):
    logging.info("Получена команда \\start")
    ul(update.effective_user, context.user_data)
    text, reply_markup = il.start_command(update.effective_user)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def help_handler(update, context):
    logging.info("Получена команда \\help")
    ul(update.effective_user, context.user_data)
    text, reply_markup = il.help_command(update.effective_user)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def credits_handler(update, context):
    logging.info("Получена команда \\credits")
    ul(update.effective_user, context.user_data)
    text, reply_markup = il.credits_command(update.effective_user)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

#
# def language(update, context):
#     logging.info("Получена команда \\language")
#     user_id = update.effective_message.from_user.id
#     chat_id = update.effective_chat.id
#     keyboard = []
#     for locale in texter.get_locales():
#         callback_data = "lang#" + locale + "#" + str(user_id)
#         keyboard.append([InlineKeyboardButton(tr(locale), callback_data=callback_data)])
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     message = tr("choose_lang")
#     context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

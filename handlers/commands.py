import logging
from telegram.ext import CommandHandler

import interface_layout as il
from localization import ul


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков команд")
    dispatcher.add_handler(CommandHandler('credits', credits_handler))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('language', language_handler))
    dispatcher.add_handler(CommandHandler('start', start))


def help_handler(update, context):
    logging.info("Получена команда \\help")
    ul(update.effective_user, context.user_data)
    text = il.help_command()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def credits_handler(update, context):
    logging.info("Получена команда \\credits")
    ul(update.effective_user, context.user_data)
    text = il.credits_command()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def language_handler(update, context):
    logging.info("Получена команда \\language")
    ul(update.effective_user, context.user_data)
    text, reply_markup = il.language_command(context.user_data)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)


def start(update, context):
    logging.info("Получена команда \\start")
    ul(update.effective_user, context.user_data)
    text = il.start_command()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

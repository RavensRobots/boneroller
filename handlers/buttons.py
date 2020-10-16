import logging
from telegram.ext import CallbackQueryHandler

import interface_layout as il


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков кнопок")
    dispatcher.add_handler(CallbackQueryHandler(button))


def button(update, context):
    query = update.callback_query
    query.answer()
    logging.info("Нажата кнопка, информация о нажатии: %s", query.data)
    command, data = query.data.split("#")
    if command == "lang":
        text = il.set_language(context.user_data, data)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

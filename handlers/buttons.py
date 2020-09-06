import logging
from telegram.ext import CallbackQueryHandler

import manager


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков кнопок")

    dispatcher.add_handler(CallbackQueryHandler(button))


def button(update, context):
    query = update.callback_query
    query.answer()
    logging.info("Нажата кнопка, информация о нажатии: %s", query.data)
    chat_id = update.effective_chat.id
    data, details, user_id = query.data.split("#")
    result = ""
    if data == "lang":
        result = manager.set_language(user_id, details)
    elif data == "pig_new_game":
        result = manager.new_pig_game(details, user_id)
    context.bot.send_message(chat_id=chat_id, text=result)


# callback_data_turn = "pig_turn#" + str(chat_id) + "#" + str(user_id)
# callback_data_new_game = "pig_new_game#" + str(chat_id) + "#" + str(user_id)
# callback_data_join = "pig_join#" + str(chat_id) + "#" + str(user_id)

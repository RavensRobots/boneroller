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
    data, details, user_id = query.data.split("#")
    result = ""
    if data == "lang":
        result = manager.set_language(user_id, details)
    query.edit_message_text(text=result)


# def pig(update, context):
#     logging.info("Получена команда \\pig")
#     user_id = update.effective_message.from_user.id
#     chat_id = update.effective_chat.id
#     if manager.is_game_running(chat_id, "pig"):
#         keyboard = [[InlineKeyboardButton(tr("make_a_turn"), callback_data="turn")],
#                     [InlineKeyboardButton(tr("create_new"), callback_data="new_game")]]
#         message = manager.get_game_info(chat_id, "pig")
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)

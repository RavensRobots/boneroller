import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

import manager
from localization import texter, tr


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков кнопок")

    dispatcher.add_handler(CallbackQueryHandler(button))


def button(update, context):
    query = update.callback_query
    query.answer()
    logging.info("Нажата кнопка, информация о нажатии: %s", query.data)
    chat = update.effective_chat
    cid = str(chat.id)
    user = query.from_user
    uid = str(user.id)
    data, details = query.data.split("#")
    if data == "lang":
        context.bot.send_message(chat_id=cid, text=manager.set_language(uid, details))
    elif data == "pig_create":
        manager.new_pig_game(chat, user)
        query.message.reply_markup = []
        callback_data_start_game = "pig_start#"
        callback_data_join = "pig_join#"
        callback_data_leave = "pig_leave#"
        callback_data_stop = "pig_stop#"
        keyboard = [[InlineKeyboardButton(tr("start_a_game"), callback_data=callback_data_start_game)],
                    [InlineKeyboardButton(tr("join_a_game"), callback_data=callback_data_join)],
                    [InlineKeyboardButton(tr("leave_a_game"), callback_data=callback_data_leave)],
                    [InlineKeyboardButton(tr("stop_a_game"), callback_data=callback_data_stop)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=cid, text=manager.get_game_info(chat, "pig"), reply_markup=reply_markup)
    elif data == "pig_join":
        pass


# callback_data_turn = "pig_turn#" + str(chat_id) + "#" + str(user_id)
# callback_data_new_game = "pig_new_game#" + str(chat_id) + "#" + str(user_id)
# callback_data_join = "pig_join#" + str(chat_id) + "#" + str(user_id)

import logging
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

import interface


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков кнопок")

    dispatcher.add_handler(CallbackQueryHandler(button))


def button(update, context):
    query = update.callback_query
    query.answer()
    logging.info("Нажата кнопка, информация о нажатии: %s", query.data)
    chat = update.effective_chat
    cid = str(chat.id)
    user = update.effective_user
    uid = str(user.id)
    data, details = query.data.split("#")

    if data == "lang":
        pass
        # text = manager.set_language(uid, details)
        # context.bot.send_message(chat_id=cid, text=text)

    elif data == "pig_create":
        text, keyboard = interface.new_game(chat, user, "pig")
        if text != "":
            query.edit_message_text(text=text)
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_reply_markup(reply_markup=reply_markup)
    elif data == "pig_join":
        text, keyboard = interface.join_game(chat, user, "pig")
        if text != "":
            query.edit_message_text(text=text)
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_reply_markup(reply_markup=reply_markup)
    elif data == "pig_leave":
        text, keyboard = interface.leave_game(chat, user, "pig")
        if text != "":
            query.edit_message_text(text=text)
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_reply_markup(reply_markup=reply_markup)
    elif data == "pig_roll":
        text, keyboard = interface.action(chat, user, "pig", "roll")
        if text != "":
            query.edit_message_text(text=text)
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_reply_markup(reply_markup=reply_markup)
    elif data == "pig_start":
        text, keyboard = interface.start_game(chat, "pig")
        if text != "":
            query.edit_message_text(text=text)
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_reply_markup(reply_markup=reply_markup)
    elif data == "pig_stop":
        text = interface.stop_game(chat, "pig")
        if text != "":
            query.edit_message_text(text=text)
    elif data == "pig_turn":
        text, keyboard = interface.action(chat, user, "pig", "turn")
        if text != "":
            query.edit_message_text(text=text)
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_reply_markup(reply_markup=reply_markup)


#             [InlineKeyboardButton(tr("make_a_turn"), callback_data="pig_turn#")],

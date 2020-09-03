import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler

import manager
from localization import tr


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков команд")
    dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_error_handler(error)

    dispatcher.add_handler(CommandHandler('d6', d6))
    dispatcher.add_handler(CommandHandler('pig', pig))

    dispatcher.add_handler(CallbackQueryHandler(button))


def start(update, context):
    logging.info("Получена команда \\start")
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.greet())


def error(update, context):
    logging.warning("Вызван обработчик ошибок")
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.get_error_message())


def d6(update, context):
    logging.info("Получена команда \\d6")
    context.bot.send_message(chat_id=update.effective_chat.id, text=manager.roll_a_dice(6))


def pig(update, context):
    logging.info("Получена команда \\pig")
    user_id = update.effective_message.from_user.id
    chat_id = update.effective_chat.id
    if manager.is_game_running(chat_id, "pig"):
        keyboard = [[InlineKeyboardButton(tr("make_a_turn"), callback_data="turn")],
                    [InlineKeyboardButton(tr("create_new"), callback_data="new_game")]]
        message = manager.get_game_info(chat_id, "pig")
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.answer()

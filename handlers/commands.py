import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler

import operator
from localization import texter, tr


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков команд")
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('language', language))

    dispatcher.add_handler(CommandHandler('d6', d6))
    dispatcher.add_handler(CommandHandler('pig', pig))


def start(update, context):
    logging.info("Получена команда \\start")
    context.bot.send_message(chat_id=update.effective_chat.id, text=operator.greet())


def language(update, context):
    logging.info("Получена команда \\language")
    chat_id = update.effective_chat.id
    keyboard = []
    for locale in texter.get_locales():
        callback_data = "lang#" + locale
        keyboard.append([InlineKeyboardButton(tr(locale), callback_data=callback_data)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = tr("choose_lang")
    context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


def d6(update, context):
    logging.info("Получена команда \\d6")
    context.bot.send_message(chat_id=update.effective_chat.id, text=operator.roll_a_dice(6))


def pig(update, context):
    logging.info("Получена команда \\pig")
    chat = update.effective_chat
    user = update.effective_user
    cid = str(chat.id)
    if chat.type == "group" or chat.type == "supergroup":
        text, keyboard = operator.get_game(chat, user, "pig")
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=cid, text=text, reply_markup=reply_markup)
    elif chat.type == "private":
        context.bot.send_message(chat_id=cid, text=tr("command_for_group"))

    # if not manager.is_game_running(chat, "pig"):
    #     callback_data_create_game = "pig_create#"
    #     keyboard = [[InlineKeyboardButton(tr("create_new"), callback_data=callback_data_create_game)]]
    #     message = tr("no_pig_game")
    #     reply_markup = InlineKeyboardMarkup(keyboard)
    #     context.bot.send_message(chat_id=cid, text=message, reply_markup=reply_markup)

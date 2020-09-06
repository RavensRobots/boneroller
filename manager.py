import logging

import dicer
from pig import pig
from localization import tr, texter
from user_data import sl, gl


def get_error_message():
    logging.info("Подготовка сообщения об ошибке")
    return tr("error")


def get_game_info(chat_id, game):
    if game == "pig":
        return pig.get_info(chat_id)
    return tr("game_pig")


def greet():
    logging.info("Подготовка сообщения с приветствием")
    return tr("greetings")


def is_game_running(chat_id, game):
    logging.info("Проверка того, запущена ли игра %s в чате %s", game, chat_id)
    if game == "pig" and pig.is_game_running(chat_id):
        return True
    return False


def new_pig_game(chat_id, user_id):
    logging.info("Создание новой игры 'Свин', чат: {}, создатель: {}".format(chat_id, user_id))
    pig.new_game(chat_id, user_id)
    return tr("game_created")


def roll_a_dice(n):
    logging.info("Подготовка сообщения с броском кубика с количеством граней %d", n)
    if n > 0:
        return dicer.d(n)


def set_language(user_id, locale):
    logging.info("Подготовка ответа на смену языка, пользователь %s, язык %s", user_id, locale)
    sl(user_id, locale)
    texter.set_locale(gl(user_id))
    return tr("lang_changed").format(tr(locale))

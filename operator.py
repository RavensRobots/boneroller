import logging

import dicer
from pig import pig
from localization import tr, texter
from user_data import sl, gl


def get_error_message():
    logging.info("Подготовка сообщения об ошибке")
    return tr("error")


def get_game(chat, user, game):
    logging.info("Получаем игру {} в чате {}, инициатор: {}".format(game, str(chat.id), str(user.id)))
    if game == "pig":
        return pig.get_game(chat, user)
    else:
        return "", []


def get_game_info(chat, game):
    if game == "pig":
        return pig.get_info(chat)
    return pig.get_info(chat)


def join_a_game(chat, user, game):
    if game == "pig":
        pass


def greet():
    logging.info("Подготовка сообщения с приветствием")
    return tr("greetings")


def is_game_running(chat, game):
    logging.info("Проверка того, запущена ли игра %s в чате %s", game, str(chat.id))
    return game == "pig" and pig.is_game_running(chat)


def new_pig_game(chat, user):
    logging.info("Создание новой игры 'Свин', чат: {}, создатель: {}".format(str(chat.id), str(user.id)))
    pig.new_game(chat, user)


def roll_a_dice(n):
    logging.info("Подготовка сообщения с броском кубика с количеством граней %d", n)
    if n > 0:
        return dicer.d(n)


def set_language(user_id, locale):
    logging.info("Подготовка ответа на смену языка, пользователь %s, язык %s", user_id, locale)
    sl(user_id, locale)
    texter.set_locale(gl(user_id))
    return tr("lang_changed").format(tr(locale))

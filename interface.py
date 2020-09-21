import logging

# import dicer
from pig import pig
# from localization import tr, texter
# from user_data import sl, gl


def action(chat, user, game, action_type):
    logging.info("Пользователь {} совершает действие {} в игре {} в чате {}"
                 .format(str(user.id), action_type, game, str(chat.id)))
    if game == "pig":
        return pig.action(chat, user, action_type)
    else:
        return "", []


def join_game(chat, user, game):
    logging.info("Пользователь {} пытается присоединиться к игре {} в чате {}".format(str(user.id), game, str(chat.id)))
    if game == "pig":
        return pig.join_game(chat, user)
    else:
        return "", []


def get_game(chat, user, game):
    logging.info("Получаем игру {} в чате {}, инициатор: {}".format(game, str(chat.id), str(user.id)))
    if game == "pig":
        return pig.get_game(chat, user)
    else:
        return "", []


def leave_game(chat, user, game):
    logging.info("Пользователь {} пытается покинуть игру {} в чате {}".format(str(user.id), game, str(chat.id)))
    if game == "pig":
        return pig.leave_game(chat, user)
    else:
        return "", []


def new_game(chat, user, game):
    logging.info("Создаем игру {} в чате {}, инициатор: {}".format(game, str(chat.id), str(user.id)))
    if game == "pig":
        return pig.new_game(chat, user)
    else:
        return "", []


def start_game(chat, game):
    logging.info("Начинаем игру {} в чате {}".format(game, str(chat.id)))
    if game == "pig":
        return pig.start_game(chat)
    else:
        return "", []


def stop_game(chat, game):
    logging.info("Завершаем игру {} в чате {}".format(game, str(chat.id)))
    if game == "pig":
        return pig.stop_game(chat)
    else:
        return "", []

# def get_game_info(chat, game):
#     if game == "pig":
#         return pig.get_info(chat)
#     return pig.get_info(chat)
#
#
# def greet():
#     logging.info("Подготовка сообщения с приветствием")
#     return tr("greetings")
#
#
# def is_game_running(chat, game):
#     logging.info("Проверка того, запущена ли игра %s в чате %s", game, str(chat.id))
#     return game == "pig" and pig.is_game_running(chat)
#
#
# def new_pig_game(chat, user):
#     logging.info("Создание новой игры 'Свин', чат: {}, создатель: {}".format(str(chat.id), str(user.id)))
#     pig.new_game(chat, user)
#
#
# def roll_a_dice(n):
#     logging.info("Подготовка сообщения с броском кубика с количеством граней %d", n)
#     if n > 0:
#         return dicer.d(n)
#
#
# def set_language(user_id, locale):
#     logging.info("Подготовка ответа на смену языка, пользователь %s, язык %s", user_id, locale)
#     sl(user_id, locale)
#     texter.set_locale(gl(user_id))
#     return tr("lang_changed").format(tr(locale))

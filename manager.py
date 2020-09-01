import dicer
from localization import texter, tr


def get_error_message():
    return tr("error")


def greet():
    return tr("greetings")


def is_game_running(chat_id, game):
    return False


def roll_a_dice(n):
    if n > 0:
        return dicer.d(n)

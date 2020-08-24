import dicer


def greet():
    return "Привет, кинь кубик через команду /d6"


def roll_a_dice(n):
    if n > 0:
        return dicer.d(n)


def get_error_message():
    return "Неизвестная ошибка"

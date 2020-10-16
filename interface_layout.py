from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from dicer import d
from localization import texter, tr


def start_command():
    return tr("start_message")


def help_command():
    return tr("help_message")


def credits_command():
    return tr("credits_message")


def language_command(user_data):
    keyboard = []
    for locale in texter.get_locales():
        if user_data["language"] != locale:
            callback_data = "lang#" + locale
            keyboard.append([InlineKeyboardButton(tr(locale), callback_data=callback_data)])
    return tr("language_message"), InlineKeyboardMarkup(keyboard)


def set_language(user_data, locale):
    user_data["language"] = locale
    texter.set_locale(locale)
    return tr("language_set")


def roll(sides):
    return tr("roll").format(sides) + str(d(sides))

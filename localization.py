import json
import logging
import os


class Texter(object):

    def __init__(self):
        self.locales = load_locales("locales")
        self.default_locale = "EN"
        self.locale = self.default_locale

    def set_locale(self, locale):
        logging.info("Установлена новая локализация: %s", locale)
        self.locale = locale

    def get_text_for_label(self, label):
        logging.info("Получение текста для метки: %s", label)
        if self.locale in self.locales and label in self.locales[self.locale]:
            logging.info("Текст для текущей локализации: %s", self.locales[self.locale][label])
            return self.locales[self.locale][label]
        elif self.default_locale in self.locales and label in self.locales[self.default_locale]:
            logging.info("Текст для локализации по умолчанию: %s", self.locales[self.default_locale][label])
            return self.locales[self.default_locale][label]
        else:
            logging.warning("Отсутствует текст для метки %s", label)
            return "UNDEFINED"


def load_locales(directory):
    result = {}
    for dirpath, unused, filenames in os.walk(directory):
        for filename in filenames:
            file = open(os.path.join(dirpath, filename), "r")
            json_data = file.read()
            data = json.loads(json_data)
            result[data["locale"]] = data["values"]
    return result


texter = Texter()
tr = texter.get_text_for_label

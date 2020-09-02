import logging
import random


def d(n):
    logging.info("Бросок кубика с количеством граней %d", n)
    random_number = random.randint(1, n)
    logging.info("Результат: %d", random_number)
    return random_number

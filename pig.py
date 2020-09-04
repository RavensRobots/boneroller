import logging

import game_exception as gexp
from localization import tr


class PigManager(object):

    def __init__(self):
        self.games = {}

    def new_game(self, chat_id, user_id):
        logging.info("Создание игры")
        self.games[chat_id] = PigGame()
        self.games[chat_id].join(user_id)

    def is_game_running(self, chat_id):
        logging.info("Проверка запущенной игры")
        if str(chat_id) in self.games:
            return True
        else:
            return False

    def get_info(self, chat_id):
        return self.games[str(chat_id)].info()


class PigGame(object):

    def __init__(self, user):
        uid = str(user.id)
        self.started = False
        self.players = {uid: Player(get_name(user))}
        self.queue = [uid]
        self.current_player = uid
        self.current_score = 0
        self.players_above = []

    def join(self, user):
        uid = str(user.id)
        logging.info("Добавление игрока {} в игру".format(uid))

        if self.started:
            logging.warning("Игра уже начата")
            raise gexp.GameStarted
        if uid in self.players:
            logging.warning("Игрок {} уже присоединился к этой игре".format(uid))
            raise gexp.AlreadyJoined

        self.players[uid] = Player(get_name(user))
        self.queue.append(uid)
        if self.current_player is None:
            self.current_player = uid

    def left(self, user):
        uid = str(user.id)
        logging.info("Удаление игрока {} из игры".format(uid))

        if uid not in self.players:
            logging.warning("Игрок {} не является участником игры".format(uid))
            return

        del self.players[uid]
        if self.current_player == uid:
            if len(self.queue) < 2:
                self.current_player = None
            else:
                next_index = 1
                for pl in self.queue:
                    if next_index == len(self.queue):
                        next_index = 0
                    next_pl = self.queue[next_index]
                    if pl == uid:
                        self.current_player = next_pl
                        break
                    next_index += 1
        self.queue.remove(uid)
        if uid in self.players_above:
            self.players_above.remove(uid)

    def info(self):
        logging.info("Формирование информации об игре")
        message = tr("players") + "\n"
        for player in self.players:
            message = message + player + "\n"
        return message


class Player(object):

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.priority = 0


def get_name(user):
    return user.first_name if user.username is None else user.username


pig = PigManager()

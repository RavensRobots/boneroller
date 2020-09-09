import logging

import dicer
import game_exception as gexp
from localization import tr


class PigManager(object):

    def __init__(self):
        self.games = {}

    def new_game(self, chat, user):
        logging.info("Создание игры")
        self.games[chat.id] = PigGame(user)

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
        self.queue = [uid]
        self.players = {uid: Player(get_name(user))}

    def join(self, user):
        uid = str(user.id)
        logging.info("Добавление игрока {} в игру".format(uid))

        if self.started:
            logging.warning("Игра уже начата")
            raise gexp.GameStarted
        if uid in self.players:
            logging.warning("Игрок {} уже присоединился к этой игре".format(uid))
            raise gexp.AlreadyJoined

        self.queue.append(uid)
        self.players[uid] = Player(get_name(user))

    def left(self, user):
        uid = str(user.id)
        logging.info("Удаление игрока {} из игры".format(uid))

        if uid not in self.players:
            logging.warning("Игрок {} не является участником игры".format(uid))
            raise gexp.PlayerNotInGame

        self.queue.remove(uid)
        del self.players[uid]
        for pl in self.queue:
            if uid in self.players[pl].players_above:
                self.players[pl].players_above.remove(uid)
        if len(self.queue) == 1 and self.started:
            raise gexp.PlayerWin(self.queue[0])

    def start(self):
        logging.info("Игрок запускает игру")

        if self.started:
            logging.warning("Игра уже запущена")
            raise gexp.GameStarted

        if len(self.queue) < 2:
            logging.warning("Недостаточно игроков")
            raise gexp.NotEnoughPlayers

        self.started = True

    def end_turn(self, user):
        uid = str(user.id)
        logging.info("Игрок {} завершает ход".format(uid))

        if not self.started:
            logging.warning("Ход не может быть завершен, игра не начата")
            raise gexp.GameNotStarted

        if uid not in self.players:
            logging.warning("Игрок {} не является участником игры".format(uid))
            raise gexp.PlayerNotInGame

        if self.queue[0] != uid:
            logging.warning("Игрок {} не является текущим".format(uid))
            raise gexp.PlayerNotCurrent

        self.queue.remove(uid)
        self.queue.append(uid)

        if self.players[uid].score == 0:
            for pl in self.queue:
                if uid != pl and self.players[pl].score == 0:
                    self.players[pl].players_above.append(uid)

        if self.players[uid].current_score == 0:
            self.players[uid].score += 3
            raise gexp.PlayerIsNotRisking

        self.players[uid].score += self.players[uid].current_score
        self.players[uid].current_score = 0

        if self.players[uid].score > 100:
            raise gexp.PlayerWin(uid)

    def roll(self, user):
        uid = str(user.id)
        logging.info("Игрок {} бросает кубик".format(uid))

        if not self.started:
            logging.warning("Игрок не может ходить, игра не начата")
            raise gexp.GameNotStarted

        if uid not in self.players:
            logging.warning("Игрок {} не является участником игры".format(uid))
            raise gexp.PlayerNotInGame

        if self.queue[0] != uid:
            logging.warning("Игрок {} не является текущим".format(uid))
            raise gexp.PlayerNotCurrent

        roll_result = dicer.d(6)
        if roll_result > 1:
            self.players[uid].current_score += roll_result

    def info(self):
        message = tr("game_pig") + "\n"
        message += tr("started") if self.started else tr("not_started")

        message += tr("players") + "\n"
        sorted_queue = sorted(self.queue, key=lambda player: self.players[player].score, reverse=True)
        for pl in sorted_queue:
            message += self.players[pl].name + " - " + str(self.players[pl].score) + "\n"

        message += tr("current_player") + "\n"
        message += self.players[self.queue[0]].name + str(self.players[self.queue[0]].score) + "\n"
        message += tr("current_score") + str(self.players[self.queue[0]].current_score)

        return message


class Player(object):

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_score = 0
        self.players_above = []


def get_name(user):
    return user.first_name if user.username is None else user.username


pig = PigManager()

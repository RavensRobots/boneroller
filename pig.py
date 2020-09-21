import logging
from telegram import InlineKeyboardButton

import dicer
import game_exception as gexp
from localization import tr


class PigInterface(object):

    def __init__(self):
        self.games = {}

    def action(self, chat, user, action_type):
        uid = str(user.id)
        cid = str(chat.id)
        if cid in self.games:
            game = self.games[cid]
            if action_type == "roll":
                text = ""
                try:
                    game.roll(user)
                except gexp.FailedRoll:
                    text += tr("failed_roll") + "\n\n"
                except gexp.GameException:
                    return "", []
                text += game.info()
                keyboard = [[InlineKeyboardButton(tr("roll_a_dice"), callback_data="pig_roll#")],
                            [InlineKeyboardButton(tr("make_a_turn"), callback_data="pig_turn#")],
                            [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")],
                            [InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")]]
                return text, keyboard
            elif action_type == "turn":
                text = ""
                try:
                    game.end_turn(user)
                except gexp.PlayerIsNotRisking:
                    text += tr("player_is_not_risking") + "\n\n"
                except gexp.PlayerWin as e:
                    text = tr("player_win").format(e.winner)
                    return text, []
                except gexp.GameException:
                    return "", []
                text += game.info()
                keyboard = [[InlineKeyboardButton(tr("roll_a_dice"), callback_data="pig_roll#")],
                            [InlineKeyboardButton(tr("make_a_turn"), callback_data="pig_turn#")],
                            [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")],
                            [InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")]]
                return text, keyboard

    def join_game(self, chat, user):
        uid = str(user.id)
        cid = str(chat.id)
        logging.info("Пользователь {} пытается присоединиться к игре".format(uid))
        if cid in self.games:
            game = self.games[cid]
            try:
                game.join(user)
            except gexp.GameException:
                return "", []
            text = game.info()
            keyboard = [[InlineKeyboardButton(tr("join_a_game"), callback_data="pig_join#")],
                        [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")]]
            if len(game.queue) > 1:
                keyboard.append([InlineKeyboardButton(tr("start_a_game"), callback_data="pig_start#")])
            keyboard.append([InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")])
            return text, keyboard
        else:
            logging.warning("Нет запущенной игры")
        return "", []

    def get_game(self, chat, user):
        logging.info("Проверяем наличие игры")
        cid = str(chat.id)
        if cid not in self.games:
            logging.info("В этом чате нет игры")
            text = tr("no_pig_game")
            keyboard = [[InlineKeyboardButton(tr("create_new"), callback_data="pig_create#")]]
            return text, keyboard
        else:
            logging.info("Игра найдена")
            pass

    def leave_game(self, chat, user):
        uid = str(user.id)
        cid = str(chat.id)
        logging.info("Пользователь {} пытается покинуть игру".format(uid))
        if cid in self.games:
            game = self.games[cid]
            try:
                game.leave(user)
            except gexp.PlayerWin as e:
                text = tr("player_win").format(e.winner)
                return text, []
            except gexp.GameException:
                return "", []
            text = game.info()
            if not game.started:
                keyboard = [[InlineKeyboardButton(tr("join_a_game"), callback_data="pig_join#")],
                            [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")]]
                if len(game.queue) > 1:
                    keyboard.append([InlineKeyboardButton(tr("start_a_game"), callback_data="pig_start#")])
                keyboard.append([InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")])
            else:
                keyboard = [[InlineKeyboardButton(tr("roll_a_dice"), callback_data="pig_roll#")],
                            [InlineKeyboardButton(tr("make_a_turn"), callback_data="pig_turn#")],
                            [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")],
                            [InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")]]
            return text, keyboard
        return "", []

    def new_game(self, chat, user):
        logging.info("Создание игры")
        cid = str(chat.id)
        self.games[cid] = PigGame(user)
        text = tr("game_created") + "\n\n" + self.games[cid].info()
        keyboard = [[InlineKeyboardButton(tr("join_a_game"), callback_data="pig_join#")],
                    [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")],
                    [InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")]]
        return text, keyboard

    def start_game(self, chat):
        logging.info("Запуск игры")
        cid = str(chat.id)
        self.games[cid].start()
        text = tr("game_started") + "\n\n" + self.games[cid].info()
        keyboard = [[InlineKeyboardButton(tr("roll_a_dice"), callback_data="pig_roll#")],
                    [InlineKeyboardButton(tr("make_a_turn"), callback_data="pig_turn#")],
                    [InlineKeyboardButton(tr("leave_a_game"), callback_data="pig_leave#")],
                    [InlineKeyboardButton(tr("stop_a_game"), callback_data="pig_stop#")]]
        return text, keyboard

    def stop_game(self, chat):
        logging.info("Остановка игры")
        cid = str(chat.id)
        del self.games[cid]
        text = tr("game_stopped")
        return text


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

    def leave(self, user):
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
            raise gexp.PlayerWin(self.players[self.queue[0]].name)

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
        else:
            self.players[uid].current_score = 0
            self.queue.remove(uid)
            self.queue.append(uid)
            raise gexp.FailedRoll

    def info(self):
        message = tr("players") + " - " + tr("score") + ":\n"
        sorted_queue = sorted(self.queue, key=lambda player: self.players[player].score, reverse=True)
        for pl in sorted_queue:
            message += self.players[pl].name + " - " + str(self.players[pl].score) + "\n"

        if self.queue:
            message += "\n" + tr("current_player") + " - " + self.players[self.queue[0]].name + "\n\n"
            message += tr("current_score") + " - " + str(self.players[self.queue[0]].current_score)

        return message


class Player(object):

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.current_score = 0
        self.players_above = []


def get_name(user):
    return user.first_name if user.username is None else user.username


pig = PigInterface()

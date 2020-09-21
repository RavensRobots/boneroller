class GameException(Exception):
    pass


class AlreadyJoined(GameException):
    pass


class FailedRoll(GameException):
    pass


class GameStarted(GameException):
    pass


class GameNotStarted(GameException):
    pass


class NotEnoughPlayers(GameException):
    pass


class PlayerIsNotRisking(GameException):
    pass


class PlayerNotCurrent(GameException):
    pass


class PlayerNotInGame(GameException):
    pass


class PlayerWin(GameException):

    def __init__(self, winner):
        self.winner = winner

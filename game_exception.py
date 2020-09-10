class AlreadyJoined(Exception):
    pass


class GameStarted(Exception):
    pass


class GameNotStarted(Exception):
    pass


class PlayerNotInGame(Exception):
    pass


class PlayerNotCurrent(Exception):
    pass


class PlayerIsNotRisking(Exception):
    pass


class NotEnoughPlayers(Exception):
    pass


class FailedRoll(Exception):
    pass


class PlayerWin(Exception):

    def __init__(self, winner):
        self.winner = winner

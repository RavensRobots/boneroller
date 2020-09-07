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


class PlayerHas0(Exception):
    pass


class PlayerWin(Exception):

    def __init__(self, winner):
        self.winner = winner

import unittest
from unittest import mock

import dicer
import game_exception as gexp
import pig


class TestJoin(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()

    def test_no_players(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)
        del game.players[user_id]
        game.queue.remove(user_id)

        game.join(self.user)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_one_player(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"

        game.join(self.user2)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id, user_id2])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, 0)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(len(game.players[user_id2].players_above), 0)

    def test_player_already_joined(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        with self.assertRaises(gexp.AlreadyJoined):
            game.join(self.user)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_game_is_started(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.started = True

        self.user2.id = 234567
        self.user2.username = "user_name2"

        with self.assertRaises(gexp.GameStarted):
            game.join(self.user2)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)


class TestLeft(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()

    def test_player_not_in_game(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        self.user2.username = "user_name2"

        with self.assertRaises(gexp.PlayerNotInGame):
            game.left(self.user2)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_player_only_one(self):
        self.user.id = 123456
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.left(self.user)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [])
        self.assertEqual(game.players, {})

    def test_current_player_first(self):
        self.user.id = 123456
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        game.left(self.user)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id2])

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, 0)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(len(game.players[user_id2].players_above), 0)

    def test_current_player_last(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        self.user2.username = "user_name2"
        game.join(self.user2)

        game.left(self.user2)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_game_running_and_two_players(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        self.user2.username = "user_name2"
        game.join(self.user2)

        game.start()

        with self.assertRaises(gexp.PlayerWin) as pw:
            game.left(self.user2)

        self.assertEqual(user_id, pw.exception.winner)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_player_was_above(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)
        game.players[user_id].players_above.append(user_id2)

        game.left(self.user2)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)


class TestStart(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()

    def test_game_already_started(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.started = True

        with self.assertRaises(gexp.GameStarted):
            game.start()

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_player_only_one(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        with self.assertRaises(gexp.NotEnoughPlayers):
            game.start()

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_success(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        game.start()

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id, user_id2])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, 0)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(len(game.players[user_id2].players_above), 0)


class TestEndTurn(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()
        self.user3 = User()

    def test_game_not_started(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        with self.assertRaises(gexp.GameNotStarted):
            game.end_turn(self.user2)

        self.assertFalse(game.started)
        self.assertEqual(game.queue, [user_id, user_id2])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, 0)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(len(game.players[user_id2].players_above), 0)

    def test_player_not_in_game(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.started = True

        self.user2.id = 234567
        self.user2.username = "user_name2"

        with self.assertRaises(gexp.PlayerNotInGame):
            game.end_turn(self.user2)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_player_not_current(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        game.start()

        with self.assertRaises(gexp.PlayerNotCurrent):
            game.end_turn(self.user2)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id, user_id2])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, 0)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, 0)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(len(game.players[user_id2].players_above), 0)

    def test_player_first(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        self.user3.id = 345678
        user_id3 = str(self.user3.id)
        self.user3.username = "user_name3"
        game.join(self.user3)

        current_score = 10
        game.players[user_id].current_score = current_score
        game.start()

        game.end_turn(self.user)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id2, user_id3, user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, current_score)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, 0)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(game.players[user_id2].players_above, [user_id])

        self.assertEqual(game.players[user_id3].name, self.user3.username)
        self.assertEqual(game.players[user_id3].score, 0)
        self.assertEqual(game.players[user_id3].current_score, 0)
        self.assertEqual(game.players[user_id3].players_above, [user_id])

    def test_player_second(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        self.user3.id = 345678
        user_id3 = str(self.user3.id)
        self.user3.username = "user_name3"
        game.join(self.user3)

        score1 = 10
        game.players[user_id].score = score1
        current_score = 8
        game.players[user_id2].current_score = current_score
        game.players[user_id2].players_above = [user_id]
        game.players[user_id3].players_above = [user_id]
        game.queue = [user_id2, user_id3, user_id]
        game.start()

        game.end_turn(self.user2)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id3, user_id, user_id2])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, score1)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, current_score)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(game.players[user_id2].players_above, [user_id])

        self.assertEqual(game.players[user_id3].name, self.user3.username)
        self.assertEqual(game.players[user_id3].score, 0)
        self.assertEqual(game.players[user_id3].current_score, 0)
        self.assertEqual(game.players[user_id3].players_above, [user_id, user_id2])

    def test_player_third(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        self.user3.id = 345678
        user_id3 = str(self.user3.id)
        self.user3.username = "user_name3"
        game.join(self.user3)

        score1 = 10
        game.players[user_id].score = score1
        score2 = 8
        game.players[user_id2].score = score2
        current_score = 6
        game.players[user_id3].current_score = current_score
        game.players[user_id2].players_above = [user_id]
        game.players[user_id3].players_above = [user_id, user_id2]
        game.queue = [user_id3, user_id, user_id2]
        game.start()

        game.end_turn(self.user3)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id, user_id2, user_id3])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, score1)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

        self.assertEqual(game.players[user_id2].name, self.user2.username)
        self.assertEqual(game.players[user_id2].score, score2)
        self.assertEqual(game.players[user_id2].current_score, 0)
        self.assertEqual(game.players[user_id2].players_above, [user_id])

        self.assertEqual(game.players[user_id3].name, self.user3.username)
        self.assertEqual(game.players[user_id3].score, current_score)
        self.assertEqual(game.players[user_id3].current_score, 0)
        self.assertEqual(game.players[user_id3].players_above, [user_id, user_id2])

    def test_has_0_current_score(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.started = True

        score = 42
        score_for_not_risking = 3
        game.players[user_id].score = score

        with self.assertRaises(gexp.PlayerIsNotRisking):
            game.end_turn(self.user)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, score + score_for_not_risking)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)

    def test_player_reaches_100(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.started = True

        score = 90
        current_score = 11
        game.players[user_id].score = score
        game.players[user_id].current_score = current_score

        with self.assertRaises(gexp.PlayerWin) as exp:
            game.end_turn(self.user)

        self.assertEqual(user_id, exp.exception.winner)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, score + current_score)
        self.assertEqual(game.players[user_id].current_score, 0)
        self.assertEqual(len(game.players[user_id].players_above), 0)


class TestRoll(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()
        self.user3 = User()

    def test_roll_n(self):
        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        game.started = True

        score = 30
        current_score = 7
        game.players[user_id].score = score
        game.players[user_id].current_score = current_score

        dicer.d = mock.MagicMock()
        roll_result = 3
        dicer.d.return_value = roll_result

        game.roll(self.user)

        dicer.d.assert_called_once_with(6)

        self.assertTrue(game.started)
        self.assertEqual(game.queue, [user_id])

        self.assertEqual(game.players[user_id].name, self.user.username)
        self.assertEqual(game.players[user_id].score, score)
        self.assertEqual(game.players[user_id].current_score, current_score + roll_result)
        self.assertEqual(len(game.players[user_id].players_above), 0)

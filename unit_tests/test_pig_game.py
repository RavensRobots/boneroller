import unittest
from unittest import mock

import pig
import game_exception as gexp


class TestJoin(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()

    def test_no_players(self):
        self.user.id = 123456
        self.user.username = "user_name"
        user_id = str(self.user.id)
        game = pig.PigGame(self.user)
        del game.players[user_id]
        game.queue.remove(user_id)
        game.current_player = None

        pig.Player = mock.MagicMock()

        game.join(self.user)

        pig.Player.assert_called_once_with(self.user.username)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

    def test_one_player(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"

        game.join(self.user2)

        pig.Player.assert_called_with(self.user2.username)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id, user_id2]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

    def test_player_already_joined(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        with self.assertRaises(gexp.AlreadyJoined):
            game.join(self.user)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

    def test_game_is_started(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)
        game.started = True

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        self.user2.username = "user_name2"

        with self.assertRaises(gexp.GameStarted):
            game.join(self.user2)

        self.assertTrue(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)


class TestLeft(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()

    def test_player_not_in_game(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        self.user2.username = "user_name2"

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

        with self.assertRaises(gexp.PlayerNotInGame):
            game.left(self.user2)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

    def test_player_only_one(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        game.left(self.user)

        self.assertFalse(game.started)
        result_players = {}
        self.assertEqual(game.players, result_players)
        result_queue = []
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, None)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

    def test_current_player_first(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        pig.Player.assert_called_with(self.user2.username)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id, user_id2]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

        game.left(self.user)

        self.assertFalse(game.started)
        result_players = {user_id2: pig.Player()}
        self.assertEqual(game.players, result_players)
        result_queue = [user_id2]
        self.assertEqual(game.queue, result_queue)
        self.assertEqual(game.current_player, user_id2)
        self.assertEqual(game.current_score, 0)
        self.assertEqual(len(game.players_above), 0)

    def test_current_player_last(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)
        game.current_player = user_id2

        pig.Player.assert_called_with(self.user2.username)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id, user_id2]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id2, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

        game.left(self.user2)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

    def test_game_running_and_two_players(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)
        game.current_player = user_id2

        pig.Player.assert_called_with(self.user2.username)

        game.started = True
        self.assertTrue(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id, user_id2]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id2, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

        with self.assertRaises(gexp.PlayerWin) as pw:
            game.left(self.user2)

        self.assertEqual(user_id, pw.exception.winner)

        self.assertTrue(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))


class TestEndTurn(unittest.TestCase):

    def setUp(self):
        class User(object):
            pass
        self.user = User()
        self.user2 = User()

    def test_game_not_started(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)
        game.current_player = user_id2

        pig.Player.assert_called_with(self.user2.username)

        game.started = False
        self.assertFalse(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id, user_id2]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id2, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

        with self.assertRaises(gexp.GameNotStarted):
            game.end_turn(self.user2)

        self.assertFalse(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id, user_id2]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id2, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

    def test_player_not_in_game(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)
        game.current_player = user_id

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        self.user2.username = "user_name2"

        game.started = True
        self.assertTrue(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

        with self.assertRaises(gexp.PlayerNotInGame):
            game.end_turn(self.user2)

        self.assertTrue(game.started)
        result_players = {user_id: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

    def test_player_not_current(self):
        pig.Player = mock.MagicMock()

        self.user.id = 123456
        user_id = str(self.user.id)
        self.user.username = "user_name"
        game = pig.PigGame(self.user)

        pig.Player.assert_called_with(self.user.username)

        self.user2.id = 234567
        user_id2 = str(self.user2.id)
        self.user2.username = "user_name2"
        game.join(self.user2)

        pig.Player.assert_called_with(self.user2.username)

        game.current_player = user_id
        game.started = True
        self.assertTrue(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id, user_id2]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

        with self.assertRaises(gexp.PlayerNotCurrent):
            game.end_turn(self.user2)

        self.assertTrue(game.started)
        result_players = {user_id: pig.Player(), user_id2: pig.Player()}
        self.assertEqual(result_players, game.players)
        result_queue = [user_id, user_id2]
        self.assertEqual(result_queue, game.queue)
        self.assertEqual(user_id, game.current_player)
        self.assertEqual(0, game.current_score)
        self.assertEqual(0, len(game.players_above))

    # def test_player_has_0(self):
    #     pig.Player = mock.MagicMock()
    #
    #     self.user.id = 123456
    #     user_id = str(self.user.id)
    #     self.user.username = "user_name"
    #     game = pig.PigGame(self.user)
    #
    #     pig.Player.assert_called_with(self.user.username)
    #
    #     self.user2.id = 234567
    #     user_id2 = str(self.user2.id)
    #     self.user2.username = "user_name2"
    #     game.join(self.user2)
    #
    #     pig.Player.assert_called_with(self.user2.username)
    #
    #     game.current_player = user_id
    #     game.started = True
    #     self.assertTrue(game.started)
    #     result_players = {user_id: pig.Player(), user_id2: pig.Player()}
    #     self.assertEqual(result_players, game.players)
    #     result_queue = [user_id, user_id2]
    #     self.assertEqual(result_queue, game.queue)
    #     self.assertEqual(user_id, game.current_player)
    #     self.assertEqual(0, game.current_score)
    #     self.assertEqual(0, len(game.players_above))
    #
    #     with self.assertRaises(gexp.PlayerHas0):
    #         game.end_turn(self.user)
    #
    #     self.assertTrue(game.started)
    #     result_players = {user_id: pig.Player(), user_id2: pig.Player()}
    #     self.assertEqual(result_players, game.players)
    #     result_queue = [user_id2, user_id]
    #     self.assertEqual(result_queue, game.queue)
    #     self.assertEqual(user_id2, game.current_player)
    #     self.assertEqual(0, game.current_score)
    #     self.assertEqual(0, len(game.players_above))
    #
    #     self.assertEqual()

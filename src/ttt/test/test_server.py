import unittest

import tornado
from tornado import testing
from tornado import escape
from tornado.testing import AsyncHTTPClient
from tornado.testing import AsyncHTTPTestCase
from tornado.testing import AsyncTestCase

from ttt import run_server
from ttt import game


class Helper:
    @staticmethod
    def _create_game(self):
        body = {
        }
        body_str = escape.json_encode(body)
        response = self.fetch('/api/v1/games', method="POST", body=body_str)
        response_json = escape.json_decode(response.body)
        assert len(response_json["games"]) == 1
        game_id = response_json["games"][0]["game_id"]
        return game_id

    @staticmethod
    def create_player(self, player_name):
        body = {
            "player": [
                {
                    "player_name": player_name
                }
            ]
        }
        body_str = escape.json_encode(body)
        response = self.fetch('/api/v1/players', method="POST", body=body_str)
        response_json = escape.json_decode(response.body)
        player_list = response_json["players"]
        assert len(player_list) == 1
        player_id = player_list[0]["player_id"]
        return player_id

    @staticmethod
    def add_player(self, game_id, player_id, player_type):
        body = {
            "action_type": "add_player",
            "player_id": player_id,
            "player_type": player_type,
        }
        body_str = escape.json_encode(body)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="POST",
            body=body_str)

    @staticmethod
    def play(self, game_id, player_id, cell_id):
        body = {
            "action_type": "play",
            "player_id": player_id,
            "cell_id": cell_id,
        }
        body_str = escape.json_encode(body)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="POST",
            body=body_str)


# This test uses coroutine style.
class MyTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return run_server.make_app()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        run_server.conn.clear()

    # @tornado.testing.gen_test
    def test_http_fetch(self):
        response = self.fetch('/', method="GET")
        # self.wait()
        # client = AsyncHTTPClient(self.io_loop)
        # response = yield client.fetch("http://www.tornadoweb.org")
        # Test contents of response
        self.assertIn("tic-tak-toe", str(response.body))
        self.stop()

    def test_get_players_list_empty(self):
        response = self.fetch('/api/v1/players', method="GET")
        response_json = escape.json_decode(response.body)
        expected_response = {'players': []}
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_create_player(self):
        player_name = 'test user name'
        body = {
            "player": [
                {
                    "player_name": player_name
                }
            ]
        }
        body_str = escape.json_encode(body)
        response = self.fetch('/api/v1/players', method="POST", body=body_str)
        response_json = escape.json_decode(response.body)
        player_id_expected = 1
        expected_response = {
            "players": [
                {
                    "player_id": player_id_expected,
                    "player_name": player_name
                }
            ],
            "result": "Success",
            "message": "User {player_name} was added ({player_id_expected})".format(
                 player_name=player_name,
                 player_id_expected=player_id_expected,
             )
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_create_games(self):
        body = {
        }
        body_str = escape.json_encode(body)
        response = self.fetch('/api/v1/games', method="POST", body=body_str)
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
        "games": [
            {"game_id": game_id_expected,
             "game_status": game.GameStatusOptions.pending,
             "game_state": {
                "cell_1": None,
                "cell_2": None,
                "cell_3": None,
                "cell_4": None,
                "cell_5": None,
                "cell_6": None,
                "cell_7": None,
                "cell_8": None,
                "cell_9": None,
                "player_turn": None
            },
            "player_x": None,
            "player_o": None}
        ],
        "result":"Success",
        "message":"Game created",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_create_games_(self):
        game_id_expected = self._create_game()
        self.assertEqual(game_id_expected, 1)
        self.stop()

    def _create_player(self, player_name):
        return Helper.create_player(self, player_name)

    def _create_game(self):
        return Helper._create_game(self)

    def _add_player(self, game_id, player_id, player_type):
        return Helper.add_player(self, game_id, player_id, player_type)

    def test_create_game_with_player(self):
        game_id = self._create_game()
        player_name_x = 'test_player_name_x'
        player_id_x = self._create_player(player_name=player_name_x)
        body = {
            "action_type": "add_player",
            "player_id": player_id_x,
            "player_type": "x",
        }
        body_str = escape.json_encode(body)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="POST",
            body=body_str)
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.pending,
                 "game_state": {
                     "cell_1": None,
                     "cell_2": None,
                     "cell_3": None,
                     "cell_4": None,
                     "cell_5": None,
                     "cell_6": None,
                     "cell_7": None,
                     "cell_8": None,
                     "cell_9": None,
                     "player_turn": None
                 },
                 "player_x": player_id_x,
                 "player_o": None}
            ],
            "result": "Success",
            "message": "Game created",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_create_games_and_start(self):
        game_id = self._create_game()
        player_name_x = 'test_player_name_x'
        player_id_x = self._create_player(player_name=player_name_x)
        player_name_y = 'test_player_name_y'
        player_id_y = self._create_player(player_name=player_name_y)
        self._add_player(game_id, player_id_y, 'o')
        self._add_player(game_id, player_id_x, 'x')
        self._add_player(game_id, player_id_x, 'player_turn')
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="GET")
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.started,
                 "game_state": {
                     "cell_1": None,
                     "cell_2": None,
                     "cell_3": None,
                     "cell_4": None,
                     "cell_5": None,
                     "cell_6": None,
                     "cell_7": None,
                     "cell_8": None,
                     "cell_9": None,
                     "player_turn": player_id_x
                 },
                 "player_x": player_id_x,
                 "player_o": player_id_y}
            ],
            "result": "Success",
            "message": "Game state",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()


class TestPlayGame(AsyncHTTPTestCase):
    def get_app(self):
        return run_server.make_app()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        run_server.conn.clear()

    def test_play_one_move(self):
        game_id = Helper._create_game(self)
        player_name_x = 'test_player_name_x'
        player_id_x = Helper.create_player(self, player_name=player_name_x)
        player_name_y = 'test_player_name_y'
        player_id_y = Helper.create_player(self, player_name=player_name_y)
        Helper.add_player(self, game_id, player_id_y, 'o')
        Helper.add_player(self, game_id, player_id_x, 'x')
        Helper.add_player(self, game_id, player_id_x, 'player_turn')
        body = {
            "action_type": "play",
            "player_id": player_id_x,
            "cell_id": 1,
        }
        body_str = escape.json_encode(body)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="POST",
            body=body_str
        )
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.started,
                 "game_state": {
                     "cell_1": 'x',
                     "cell_2": None,
                     "cell_3": None,
                     "cell_4": None,
                     "cell_5": None,
                     "cell_6": None,
                     "cell_7": None,
                     "cell_8": None,
                     "cell_9": None,
                     "player_turn": player_id_y
                 },
                 "player_x": player_id_x,
                 "player_o": player_id_y}
            ],
            "result": "Success",
            "message": "Action played",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_play_two_move(self):
        game_id = Helper._create_game(self)
        player_name_x = 'test_player_name_x'
        player_id_x = Helper.create_player(self, player_name=player_name_x)
        player_name_y = 'test_player_name_y'
        player_id_y = Helper.create_player(self, player_name=player_name_y)
        Helper.add_player(self, game_id, player_id_y, 'o')
        Helper.add_player(self, game_id, player_id_x, 'x')
        Helper.add_player(self, game_id, player_id_x, 'player_turn')
        Helper.play(self, game_id, player_id_x, 1)
        Helper.play(self, game_id, player_id_y, 2)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="GET")
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.started,
                 "game_state": {
                     "cell_1": 'x',
                     "cell_2": 'o',
                     "cell_3": None,
                     "cell_4": None,
                     "cell_5": None,
                     "cell_6": None,
                     "cell_7": None,
                     "cell_8": None,
                     "cell_9": None,
                     "player_turn": player_id_x
                 },
                 "player_x": player_id_x,
                 "player_o": player_id_y}
            ],
            "result": "Success",
            "message": "Game state",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_play_to_win(self):
        game_id = Helper._create_game(self)
        player_name_x = 'test_player_name_x'
        player_id_x = Helper.create_player(self, player_name=player_name_x)
        player_name_y = 'test_player_name_y'
        player_id_y = Helper.create_player(self, player_name=player_name_y)
        Helper.add_player(self, game_id, player_id_y, 'o')
        Helper.add_player(self, game_id, player_id_x, 'x')
        Helper.add_player(self, game_id, player_id_x, 'player_turn')
        Helper.play(self, game_id, player_id_x, 1)
        Helper.play(self, game_id, player_id_y, 5)
        Helper.play(self, game_id, player_id_x, 2)
        Helper.play(self, game_id, player_id_y, 6)
        Helper.play(self, game_id, player_id_x, 3)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="GET")
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.ended,
                 "game_state": {
                     "cell_1": 'x',
                     "cell_2": 'x',
                     "cell_3": 'x',
                     "cell_4": None,
                     "cell_5": 'o',
                     "cell_6": 'o',
                     "cell_7": None,
                     "cell_8": None,
                     "cell_9": None,
                     "player_turn": player_id_x
                 },
                 "player_x": player_id_x,
                 "player_o": player_id_y}
            ],
            "result": "Success",
            "message": "Game state",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_play_to_win_o(self):
        game_id = Helper._create_game(self)
        player_name_x = 'test_player_name_x'
        player_id_x = Helper.create_player(self, player_name=player_name_x)
        player_name_y = 'test_player_name_y'
        player_id_y = Helper.create_player(self, player_name=player_name_y)
        Helper.add_player(self, game_id, player_id_y, 'o')
        Helper.add_player(self, game_id, player_id_x, 'x')
        Helper.add_player(self, game_id, player_id_x, 'player_turn')
        Helper.play(self, game_id, player_id_x, 2)
        Helper.play(self, game_id, player_id_y, 1)
        Helper.play(self, game_id, player_id_x, 3)
        Helper.play(self, game_id, player_id_y, 4)
        Helper.play(self, game_id, player_id_x, 5)
        Helper.play(self, game_id, player_id_y, 7)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="GET")
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.ended,
                 "game_state": {
                     "cell_1": 'o',
                     "cell_2": 'x',
                     "cell_3": 'x',
                     "cell_4": 'o',
                     "cell_5": 'x',
                     "cell_6": None,
                     "cell_7": 'o',
                     "cell_8": None,
                     "cell_9": None,
                     "player_turn": player_id_y
                 },
                 "player_x": player_id_x,
                 "player_o": player_id_y}
            ],
            "result": "Success",
            "message": "Game state",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

    def test_play_to_tie(self):
        game_id = Helper._create_game(self)
        player_name_x = 'test_player_name_x'
        player_id_x = Helper.create_player(self, player_name=player_name_x)
        player_name_y = 'test_player_name_y'
        player_id_y = Helper.create_player(self, player_name=player_name_y)
        Helper.add_player(self, game_id, player_id_y, 'o')
        Helper.add_player(self, game_id, player_id_x, 'x')
        Helper.add_player(self, game_id, player_id_x, 'player_turn')
        Helper.play(self, game_id, player_id_x, 1)
        Helper.play(self, game_id, player_id_y, 3)
        Helper.play(self, game_id, player_id_x, 2)
        Helper.play(self, game_id, player_id_y, 4)
        Helper.play(self, game_id, player_id_x, 6)
        Helper.play(self, game_id, player_id_y, 5)
        Helper.play(self, game_id, player_id_x, 7)
        Helper.play(self, game_id, player_id_y, 8)
        Helper.play(self, game_id, player_id_x, 9)
        response = self.fetch(
            '/api/v1/games/{game_id}'.format(game_id=game_id),
            method="GET")
        response_json = escape.json_decode(response.body)
        game_id_expected = 1
        expected_response = {
            "games": [
                {"game_id": game_id_expected,
                 "game_status": game.GameStatusOptions.tie,
                 "game_state": {
                     "cell_1": 'x',
                     "cell_2": 'x',
                     "cell_3": 'o',
                     "cell_4": 'o',
                     "cell_5": 'o',
                     "cell_6": 'x',
                     "cell_7": 'x',
                     "cell_8": 'o',
                     "cell_9": 'x',
                     "player_turn": player_id_x
                 },
                 "player_x": player_id_x,
                 "player_o": player_id_y}
            ],
            "result": "Success",
            "message": "Game state",
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()


class SystemTest(AsyncHTTPTestCase):
    def get_app(self):
        return run_server.make_app()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        run_server.conn.clear()

    def test_create_two_players(self):
        player_name = 'test user name'

        body = {
            "player": [
                {
                    "player_name": player_name
                }
            ]
        }
        body_str = escape.json_encode(body)
        response = self.fetch('/api/v1/players', method="POST", body=body_str)
        player_name_2 = 'test user name 2'
        body["player"][0]["player_name"] = player_name_2
        body_str = escape.json_encode(body)
        response = self.fetch('/api/v1/players', method="POST", body=body_str)
        response = self.fetch('/api/v1/players', method="GET")
        response_json = escape.json_decode(response.body)
        expected_response = {
            "players": [
                {
                    "player_id": 1,
                    "player_name": player_name
                },
                {
                    "player_id": 2,
                    "player_name": player_name_2
                }
            ]
        }
        self.assertDictEqual(expected_response, response_json)
        self.stop()

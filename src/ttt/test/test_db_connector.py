import unittest
from ttt import db_connector


class TestPlayer(unittest.TestCase):
    def setUp(self):
        conn = db_connector.DBConnectionSQLAlchemy()
        conn.init_db()
        self.conn = conn

    def test_add_player(self):
        conn = self.conn
        player_list = conn.get_player_list()
        self.assertEqual(len(player_list), 0)
        player_name = 'docX'
        conn.create_new_player(player_name)
        player_list = conn.get_player_list()
        self.assertEqual(len(player_list), 1)
        self.assertEqual(player_list[0].name, player_name)

    def test_add_two_player(self):
        conn = self.conn
        player_1_name = 'docX'
        player_2_name = 'docY'
        conn.create_new_player(player_1_name)
        conn.create_new_player(player_2_name)
        player_list = conn.get_player_list()
        self.assertEqual(len(player_list), 2)
        self.assertSetEqual({player_list[0].name, player_list[1].name}, {player_1_name, player_2_name})


class TestGameState(unittest.TestCase):
    def setUp(self):
        conn = db_connector.DBConnectionSQLAlchemy()
        conn.init_db()
        self.conn = conn

    def test_create_game(self):
        game_1_state_1 = self.conn.create_new_game()
        game_2_state_1 = self.conn.create_new_game()
        self.assertNotEqual(game_1_state_1, game_2_state_1)
        self.assertNotEqual(game_1_state_1.game_id, game_2_state_1.game_id)
        self.assertEqual(game_1_state_1.board, game_2_state_1.board)

    def test_set_game_state(self):
        conn = self.conn
        game_state_created = conn.create_new_game()
        player_1_name = 'docX'
        player_1= conn.create_new_player(player_1_name)
        player_2_name = 'docY'
        player_2 = conn.create_new_player(player_2_name)
        game_state_created.player_x = player_1
        game_state_created.player_y = player_2
        game_state_created.player_turn = player_1
        conn.set_game_state(game_state_created.game_id, game_state_created)
        game_state_queried = conn.get_game_state(game_state_created.game_id)
        self.assertEqual(game_state_created.board, game_state_queried.board)


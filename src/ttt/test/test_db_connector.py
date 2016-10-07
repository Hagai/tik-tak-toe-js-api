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
        pass

    def test_empty_game(self):
        pass


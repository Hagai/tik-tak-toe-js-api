import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from ttt.database import model
from ttt.database.model import Base


class _Helper:
    @staticmethod
    def add_two_players(session, player_1_name='prof X', player_2_name='O dear'):
        player_1 = model.Player(player_1_name)
        session.add(player_1)
        player_2 = model.Player(player_2_name)
        session.add(player_2)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        # self.session.add(self.panel)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_one(self):
        session = Session(self.engine)
        player_name = 'prof X'
        player_1 = model.Player(player_name)
        session.add(player_1)
        session.commit()
        players = session.query(model.Player)
        player_1_get = players.one()
        self.assertEqual(player_1_get.name, player_name)

    def test_two(self):
        session = Session(self.engine)
        player_1_name = 'prof X'
        player_1 = model.Player(player_1_name)
        session.add(player_1)
        player_2_name = 'O dear'
        player_2 = model.Player(player_2_name)
        session.add(player_2)
        session.commit()
        players = session.query(model.Player)
        player_all = players.all()
        expected = [player_1, player_2]
        self.assertEqual(player_all, expected)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        # self.session.add(self.panel)
        # self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_single_board(self):
        session = Session(self.engine)
        _Helper.add_two_players(session)
        session.commit()
        player_1, player_2 = session.query(model.Player).all()
        board = model.GameState()
        session.add(board)
        session.commit()
        board.player_x = player_1
        board.player_y = player_2
        board.player_active = player_1
        session.commit()
        board_result = session.query(model.GameState).one()
        self.assertEqual(board_result.player_y.name, player_2.name)

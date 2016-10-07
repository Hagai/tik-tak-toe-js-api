"""
This module will hide the db implementation from the API server

The main responsibility of the module is to get the game state
"""
from ttt.database import model
from ttt import game
import abc

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


class DBConnectionInterface:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_player_list(self):
        pass

    @abc.abstractmethod
    def create_new_player(self, player_name):
        pass

    @abc.abstractmethod
    def create_new_game(self):
        pass

    @abc.abstractmethod
    def get_game_list(self):
        pass

    @abc.abstractmethod
    def get_game_state(self, game_id):
        """
        return the game state

        :type game_id: int
        :rtype: game.GameState
        """
        pass

    @abc.abstractmethod
    def set_game_state(self, game_id, game_state):
        """
        return the game state

        :type db_connection: DBConnection
        :type game_id: int
        :type game_state: game.GameState
        :rtype:
        """
        pass


@contextmanager
def session_scope(engine):
    """Provide a transactional scope around a series of operations."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class DBConnectionSQLAlchemy(DBConnectionInterface):
    def __init__(self, engine_path='sqlite:///:memory:'):
        self.engine = create_engine(engine_path)
        # create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    def _convert_player(db_player):
        """
        convert player instance return from the db to player instance recognized by the system
        :param db_player:
        :return:
        """
        game_player = game.Player(db_player.name)
        return game_player

    @staticmethod
    def _convert_cell(cell_value, position):
        assert cell_value in [game.CellValue.player1, game.CellValue.player2, game.CellValue.empty]
        cell = game.Cell(position, cell_value)
        return cell

    @staticmethod
    def _convert_game(db_game):
        """
        convert player instance return from the db to player instance recognized by the system
        :param db_game: a row of GameState table
        :type db_game: model.GameState
        :return:
        """
        cell1 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_1, 1)
        cell2 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_2, 2)
        cell3 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_3, 3)
        cell4 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_4, 4)
        cell5 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_5, 5)
        cell6 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_6, 6)
        cell7 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_7, 7)
        cell8 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_8, 8)
        cell9 = DBConnectionSQLAlchemy._convert_cell(db_game.cell_9, 9)
        game_board = game.GameBoard(
            cell1,
            cell2,
            cell3,
            cell4,
            cell5,
            cell6,
            cell7,
            cell8,
            cell9,
        )
        player_x = DBConnectionSQLAlchemy._convert_player(db_game.player_x)
        player_y = DBConnectionSQLAlchemy._convert_player(db_game.player_y)
        player_active = DBConnectionSQLAlchemy._convert_player(db_game.player_active)
        game_state = game.GameState(player_active,game_board, player_x, player_y)
        return game_state

    def init_db(self):
        with session_scope(self.engine) as session:
            model.Base.metadata.create_all(self.engine)

    def get_player_list(self):
        with session_scope(self.engine) as session:
            player_list = session.query(model.Player).all()
            game_player_list = [self._convert_player(player) for player in player_list]
        return game_player_list

    def create_new_player(self, player_name):
        player_instance = model.Player(player_name)
        with session_scope(self.engine) as session:
            session.add(player_instance)

    def create_new_game(self):
        player_1 = model.Player(player_1_name)
        session.add(player_1)
        pass

    def get_game_list(self):
        pass

    def get_game_state(self, game_id):
        """
        return the game state

        :type game_id: int
        :rtype: game.GameState
        """
        pass

    def set_game_state(self, game_id, game_state):
        """
        return the game state

        :type db_connection: DBConnection
        :type game_id: int
        :type game_state: game.GameState
        :rtype:
        """
        pass

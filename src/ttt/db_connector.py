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

    def clear(self):
        with session_scope(self.engine) as session:
            model.Base.metadata.drop_all(bind=self.engine)
            model.Base.metadata.create_all(bind=self.engine)

    @staticmethod
    def _convert_player(db_player):
        """
        convert player instance return from the db to player instance recognized by the system
        :param db_player:
        :return:
        """
        if db_player is None:
            game_player = None
        else:
            game_player = game.Player(db_player.name, db_player.id)
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
        game_state = game.GameState(game_board, player_active, player_x, player_y, game_id=db_game.id)
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
            session.flush()
            player = DBConnectionSQLAlchemy._convert_player(player_instance)
        return player

    def get_player(self, player_id):
        with session_scope(self.engine) as session:
            player_db = session.query(model.Player).filter(model.Player.id == player_id).one()
            player = self._convert_player(player_db)
        return player

    def create_new_game(self):
        game_state_db = model.GameState()
        with session_scope(self.engine) as session:
            session.add(game_state_db)
            session.flush()
            game_state = DBConnectionSQLAlchemy._convert_game(game_state_db)
        return game_state

    def get_game_list(self):
        with session_scope(self.engine) as session:
            game_state_db_list = session.query(model.GameState).all()
            game_state_list = [self._convert_game(game_state_db) for game_state_db in game_state_db_list]
        return game_state_list

    def get_game_state(self, game_id):
        """
        return the game state

        :type game_id: int
        :rtype: game.GameState
        """
        with session_scope(self.engine) as session:
            game_state_db = session.query(model.GameState).filter(model.GameState.id==game_id).one()
            game_state = self._convert_game(game_state_db)
        return game_state

    def _get_player_from_db(self, session, player_name):
        player = session.query(model.Player).filter(model.Player.name == player_name).one()
        return player

    def set_game_state(self, game_id, game_state):
        """
        return the game state

        :type db_connection: DBConnection
        :type game_id: int
        :type game_state: game.GameState
        :rtype: bool
        """
        with_statement_flag = False
        with session_scope(self.engine) as session:
            game_state_db = session.query(model.GameState).filter(model.GameState.id==game_id).one()
            player_x = None if (game_state.player_x is None) else self._get_player_from_db(session, game_state.player_x.name)
            game_state_db.player_x = player_x
            player_y = None if (game_state.player_y is None) else self._get_player_from_db(session, game_state.player_y.name)
            game_state_db.player_y = player_y
            player_turn = None if (game_state.player_turn is None) else self._get_player_from_db(session, game_state.player_turn.name)
            game_state_db.player_active = player_turn
            game_state_db.cell_1 = game_state.board.cell_1.value
            game_state_db.cell_2 = game_state.board.cell_2.value
            game_state_db.cell_3 = game_state.board.cell_3.value
            game_state_db.cell_4 = game_state.board.cell_4.value
            game_state_db.cell_5 = game_state.board.cell_5.value
            game_state_db.cell_6 = game_state.board.cell_6.value
            game_state_db.cell_7 = game_state.board.cell_7.value
            game_state_db.cell_8 = game_state.board.cell_8.value
            game_state_db.cell_9 = game_state.board.cell_9.value
            with_statement_flag = True
        return with_statement_flag

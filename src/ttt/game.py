"""
Game module

This module will contain all the game logic
"""

DEBUG = True


class GameStatusOptions:
    pending = "pending"
    started = "started"
    ended = "ended"
    tie = "tie"


class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.id = player_id

    def to_json(self):
        json_obj = dict(
            player_id=self.id,
            player_name=self.name,
        )
        return json_obj

    def __eq__(self, other):
        is_equal = False
        if id(self) == id(other):
            is_equal = True
        elif isinstance(other, Player):
            is_equal = other.name == self.name
        else:
            pass
        return is_equal


class CellValue:
    empty = None
    player1 = 'x'
    player2 = 'o'


class PlayerTurn:
    player1 = Player(CellValue.player1, 1)
    player2 = Player(CellValue.player2, 2)


class Cell:
    def __init__(self, place, value):
        """
        :type place: int
        :type value: CellValue
        """
        self.place = place
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Cell):
            return (other.place == self.place) and (other.value == self.value)
        else:
            return False


class GameBoard:
    def __init__(self,
                 cell_1,
                 cell_2,
                 cell_3,
                 cell_4,
                 cell_5,
                 cell_6,
                 cell_7,
                 cell_8,
                 cell_9,
                 ):
        """
        :type cell_1: Cell
        :type cell_2: Cell
        :type cell_3: Cell
        :type cell_4: Cell
        :type cell_5: Cell
        :type cell_6: Cell
        :type cell_7: Cell
        :type cell_8: Cell
        :type cell_9: Cell
        """
        self.cell_1 = cell_1
        self.cell_2 = cell_2
        self.cell_3 = cell_3
        self.cell_4 = cell_4
        self.cell_5 = cell_5
        self.cell_6 = cell_6
        self.cell_7 = cell_7
        self.cell_8 = cell_8
        self.cell_9 = cell_9
        self._cell_list = [cell_1, cell_2, cell_3, cell_4, cell_5, cell_6, cell_7, cell_8, cell_9, ]
        self._cell_dict = {_cell.place: _cell for _cell in self._cell_list}

    def get_cell_by_index(self, index):
        if (index < 1) or (index > 9):
            raise ValueError("index should be between 1 and 9 (got {index})".format(index=index))
        return self._cell_dict.get(index)

    def __eq__(self, other):
        if isinstance(other, GameBoard):
            equal = \
                (self.cell_1 == other.cell_1) and \
                (self.cell_2 == other.cell_2) and \
                (self.cell_3 == other.cell_3) and \
                (self.cell_4 == other.cell_4) and \
                (self.cell_5 == other.cell_5) and \
                (self.cell_6 == other.cell_6) and \
                (self.cell_7 == other.cell_7) and \
                (self.cell_8 == other.cell_8) and \
                (self.cell_9 == other.cell_9)
            return equal
        else:
            return False

    @classmethod
    def create_empty_board(cls):
        cell_1 = Cell(1, CellValue.empty)
        cell_2 = Cell(2, CellValue.empty)
        cell_3 = Cell(3, CellValue.empty)
        cell_4 = Cell(4, CellValue.empty)
        cell_5 = Cell(5, CellValue.empty)
        cell_6 = Cell(6, CellValue.empty)
        cell_7 = Cell(7, CellValue.empty)
        cell_8 = Cell(8, CellValue.empty)
        cell_9 = Cell(9, CellValue.empty)
        board = GameBoard(
            cell_1,
            cell_2,
            cell_3,
            cell_4,
            cell_5,
            cell_6,
            cell_7,
            cell_8,
            cell_9,
        )
        return board


class GameState:

    def __init__(self, board, player_turn=None, player_x=None, player_y=None, game_id=0):
        """
        :type player_turn: Player
        :type board: GameBoard
        :type player_x: Player
        :type player_y: Player
        :type game_id: int
        """
        self.game_id = game_id
        self.player_turn = player_turn
        self.player_x = player_x
        self.player_y = player_y
        self.board = board

    def verify_state(self):
        assert self.player_turn in [self.player_x, self.player_y]
        assert self.board.cell_1.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_2.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_3.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_4.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_5.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_6.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_7.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_8.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_9.value in [None, CellValue.player1, CellValue.player2]

    def is_pending(self):
        """
        is waiting for players to join.

        :return: True if waiting for players to join
        """
        if (self.player_y is None) or (self.player_x is None) or (self.player_turn is None):
            return True

    @staticmethod
    def get_initial_state(player_turn=PlayerTurn.player1, player_x=PlayerTurn.player1, player_y=PlayerTurn.player2):
        assert player_turn in [player_x, player_y]
        board = GameBoard.create_empty_board()
        game_status = GameState(board, player_turn, player_x, player_y)
        return game_status

    def get_game_status(self):
        if self.is_pending():
            return GameStatusOptions.pending
        elif self.is_game_won():
            return GameStatusOptions.ended
        elif self.is_play_available():
            if DEBUG:
                self.verify_state()
            return GameStatusOptions.started
        else:
            return GameStatusOptions.tie

    def to_json(self):
        if self.player_x is None:
            player_x = None
        else:
            player_x = self.player_x.id
        if self.player_y is None:
            player_y = None
        else:
            player_y = self.player_y.id

        if self.player_turn is not None:
            player_turn = self.player_turn.id
        else:
            player_turn = None
        # if (player_x is None) or (player_y is None):
        #     player_turn = None
        # elif self.player_turn == self.player_x:
        #     player_turn = player_x
        # elif self.player_turn == self.player_y:
        #     player_turn = player_y
        # else:
        #     raise RuntimeError('Illegal player turn {self.player_turn} while available players are:'
        #                        ' [{self.player_y}, {self.player_x}]'.format(self=self))
        json_obj = {
            "game_id": self.game_id,
            "game_status": self.get_game_status(),
            "game_state": {
                "cell_1": self.board.cell_1.value,
                "cell_2": self.board.cell_2.value,
                "cell_3": self.board.cell_3.value,
                "cell_4": self.board.cell_4.value,
                "cell_5": self.board.cell_5.value,
                "cell_6": self.board.cell_6.value,
                "cell_7": self.board.cell_7.value,
                "cell_8": self.board.cell_8.value,
                "cell_9": self.board.cell_9.value,
                "player_turn": player_turn,
            },
            "player_x": player_x,
            "player_o": player_y
        }
        return json_obj

    def is_game_won(self):
        victory_options = [
            [self.board.cell_1, self.board.cell_2, self.board.cell_3],
            [self.board.cell_4, self.board.cell_5, self.board.cell_6],
            [self.board.cell_7, self.board.cell_8, self.board.cell_9],

            [self.board.cell_1, self.board.cell_4, self.board.cell_7],
            [self.board.cell_2, self.board.cell_5, self.board.cell_8],
            [self.board.cell_3, self.board.cell_6, self.board.cell_9],

            [self.board.cell_1, self.board.cell_5, self.board.cell_9],
            [self.board.cell_3, self.board.cell_5, self.board.cell_7]

        ]
        is_game_end = False
        # Bad code - hard to understand.
        for cell_value in [CellValue.player1, CellValue.player2]:
            if any([
                       (all([cell.value == cell_value for cell in row]))
                       for row in victory_options
                       ]):
                is_game_end = True
        return is_game_end

    def is_play_available(self):
        has_empty_cell = any([cell.value == CellValue.empty for cell in self.board._cell_list])
        return has_empty_cell

class GameAction:
    def __init__(self, player, cell):
        """
        :type player: Player
        :type cell: Cell
        """
        self.player = player
        self.cell = cell


class GameLogic:
    @staticmethod
    def perform_action(game_state, game_action):
        """
        :type game_state: GameState
        :type game_action: GameAction
        :rtype: bool
        """
        if DEBUG:
            assert GameLogic.is_legal_action(game_state, game_action)
        current_cell_index = game_action.cell.place
        current_cell_state = game_state.board.get_cell_by_index(current_cell_index)

        if game_action.player == game_state.player_x:
            cell_value_to_use = CellValue.player1
        elif game_action.player == game_state.player_y:
            cell_value_to_use = CellValue.player2
        else:
            raise Exception("player does not exists {player}".format(player=game_action.player))
        current_cell_state.value = cell_value_to_use
        if game_state.get_game_status() == GameStatusOptions.started:
            player_turn = game_state.player_turn
            if player_turn == game_state.player_x:
                game_state.player_turn = game_state.player_y
            elif player_turn == game_state.player_y:
                game_state.player_turn = game_state.player_x
            else:
                raise RuntimeError("Invalid player {player_turn}".format(player_turn=player_turn))
        else:
            pass  # game has ended

    @staticmethod
    def is_legal_action(game_state, game_action):
        """
        :type game_state: GameState
        :type game_action: GameAction
        :rtype: bool
        """
        if DEBUG:
            game_state.verify_state()
        is_player_turn = (game_state.player_turn == game_action.player)
        if is_player_turn:
            current_cell_place = game_action.cell.place
            current_cell_state = game_state.board.get_cell_by_index(current_cell_place)
            is_legal = (current_cell_state.value == CellValue.empty)
        else:
            is_legal = False
        return is_legal

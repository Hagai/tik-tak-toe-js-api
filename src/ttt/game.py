"""
Game module
"""

DEBUG = True


class Player:
    def __init__(self, name):
        self.name = name

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
    player1 = Player(CellValue.player1)
    player2 = Player(CellValue.player2)


class Cell:
    def __init__(self, place, value):
        """
        :type place: int
        :type value: CellValue
        """
        self.place = place
        self.value = value


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
        self._cell_list = [cell_1, cell_2, cell_3, cell_4, cell_5, cell_6, cell_7, cell_8, cell_9,]
        self._cell_dict = {_cell.place: _cell for _cell in self._cell_list}

    def get_cell_by_index(self, index):
        if (index < 1) or (index > 9):
            raise ValueError("index should be between 1 and 9 (got {index})".format(index=index))
        return self._cell_dict.get(index)


class GameState:
    def __init__(self,
                 player_turn,
                 board,
                 ):
        """
        :type player_turn: Player
        :type board: GameBoard
        """
        self.player_turn = player_turn
        self.board = board
        if DEBUG:
            self.verify_state()

    def verify_state(self):
        assert self.player_turn in [PlayerTurn.player1, PlayerTurn.player2]
        assert self.board.cell_1.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_2.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_3.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_4.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_5.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_6.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_7.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_8.value in [None, CellValue.player1, CellValue.player2]
        assert self.board.cell_9.value in [None, CellValue.player1, CellValue.player2]

    @staticmethod
    def get_initial_state(player_turn=PlayerTurn.player1):
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
        game_status = GameState(
            player_turn,
            board
        )
        return game_status


class GameAction:
    def __init__(self, player, cell):
        """
        :type player: Player
        :type cell: Cell
        """
        self.player = player
        self.cell = cell


def get_status():
    pass


def add_action(player, cell_id):
    """
    in tik-tak-tow the action have two properties: (player, cell)

    :return:
    """
    pass


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
        current_cell_state.value = game_action.player.name
        player_turn = game_state.player_turn
        if player_turn == PlayerTurn.player1:
            game_state.player_turn = PlayerTurn.player2
        elif player_turn == PlayerTurn.player2:
            game_state.player_turn = PlayerTurn.player1
        else:
            raise RuntimeError("Invalid player {player_turn}".format(player_turn=player_turn))

    @staticmethod
    def is_legal_action(game_state, game_action):
        """
        :type game_state: GameState
        :type game_action: GameAction
        :rtype: bool
        """
        is_legal = True
        is_player_turn = (game_state.player_turn == game_action.player)
        if is_player_turn:
            current_cell_place = game_action.cell.place
            current_cell_state = game_state.board.get_cell_by_index(current_cell_place)
            is_legal = (current_cell_state.value == CellValue.empty)
        else:
            is_legal = False
        return is_legal
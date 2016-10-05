import unittest
from ttt import game


class TestGameStatus(unittest.TestCase):
    def test_init_state(self):
        game_state = game.GameState.get_initial_state()
        self.assertEqual(game_state.board.cell_1.value, None)
        self.assertEqual(game_state.board.cell_1.place, 1)
        self.assertEqual(game_state.board.cell_4.place, 4)
        self.assertEqual(game_state.board.cell_9.place, 9)
        self.assertEqual(game_state.player_turn, game.PlayerTurn.player1)

    def test_second_player_start(self):
        game_state = game.GameState.get_initial_state(player_turn=game.PlayerTurn.player2)
        self.assertEqual(game_state.board.cell_1.value, None)
        self.assertEqual(game_state.board.cell_1.place, 1)
        self.assertEqual(game_state.board.cell_4.place, 4)
        self.assertEqual(game_state.board.cell_9.place, 9)
        self.assertEqual(game_state.player_turn, game.PlayerTurn.player2)


class TestGameAction(unittest.TestCase):
    def test_action(self):
        game_state = game.GameState.get_initial_state()
        game_action = game.GameAction(game.PlayerTurn.player1, game_state.board.cell_1)
        game.GameLogic.perform_action(game_state, game_action)

    def test_illgal_action(self):
        game_state = game.GameState.get_initial_state()
        game_action = game.GameAction(game.PlayerTurn.player1, game_state.board.cell_1)
        game.GameLogic.perform_action(game_state, game_action)
        self.assertRaises(AssertionError, game.GameLogic.perform_action, game_state, game_action)
        game_action_2 = game.GameAction(game.PlayerTurn.player1, game_state.board.cell_2)
        self.assertRaises(AssertionError, game.GameLogic.perform_action, game_state, game_action_2)


class TestGame(unittest.TestCase):
    def test_move(self):
        game_state = game.GameState.get_initial_state()
        game_action_1 = game.GameAction(game.PlayerTurn.player1, game_state.board.cell_1)
        game_action_2 = game.GameAction(game.PlayerTurn.player2, game_state.board.cell_5)
        self.assertEqual(game_state.player_turn, game.PlayerTurn.player1)
        game.GameLogic.perform_action(game_state, game_action_1)
        self.assertEqual(game_state.player_turn, game.PlayerTurn.player2)
        game.GameLogic.perform_action(game_state, game_action_2)
        self.assertEqual(game_state.player_turn, game.PlayerTurn.player1)
        self.assertEqual(game_state.board.cell_1.value, game.CellValue.player1)
        self.assertEqual(game_state.board.cell_5.value, game.CellValue.player2)
        self.assertEqual(game_state.board.cell_2.value, game.CellValue.empty)
        self.assertEqual(game_state.board.cell_9.value, game.CellValue.empty)

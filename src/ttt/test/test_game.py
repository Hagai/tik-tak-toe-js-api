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
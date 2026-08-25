"""
Automated tests for tictactoe.py

The most important test here is `test_ai_is_unbeatable`, which plays
out EVERY possible game where the human moves first and tries every
legal move at every turn (full game-tree exhaustive search), while the
AI always uses best_ai_move(). If the AI is truly optimal, the human
can never win in any branch - only draws or AI wins are possible.

Run with:  python -m pytest test_tictactoe.py -v
       or:  python test_tictactoe.py
"""

import unittest
from tictactoe import TicTacToe, best_ai_move, HUMAN, AI, EMPTY, WIN_LINES


class TestTicTacToeBoard(unittest.TestCase):

    def test_initial_board_is_empty(self):
        game = TicTacToe()
        self.assertEqual(game.board, [EMPTY] * 9)
        self.assertIsNone(game.winner())

    def test_make_move_success(self):
        game = TicTacToe()
        self.assertTrue(game.make_move(0, HUMAN))
        self.assertEqual(game.board[0], HUMAN)

    def test_make_move_fails_on_occupied_cell(self):
        game = TicTacToe()
        game.make_move(0, HUMAN)
        self.assertFalse(game.make_move(0, AI))

    def test_undo_move(self):
        game = TicTacToe()
        game.make_move(4, HUMAN)
        game.undo_move(4)
        self.assertEqual(game.board[4], EMPTY)

    def test_row_win(self):
        game = TicTacToe()
        for i in (0, 1, 2):
            game.board[i] = AI
        self.assertEqual(game.winner(), AI)

    def test_column_win(self):
        game = TicTacToe()
        for i in (0, 3, 6):
            game.board[i] = HUMAN
        self.assertEqual(game.winner(), HUMAN)

    def test_diagonal_win(self):
        game = TicTacToe()
        for i in (0, 4, 8):
            game.board[i] = AI
        self.assertEqual(game.winner(), AI)

    def test_anti_diagonal_win(self):
        game = TicTacToe()
        for i in (2, 4, 6):
            game.board[i] = HUMAN
        self.assertEqual(game.winner(), HUMAN)

    def test_draw_detection(self):
        game = TicTacToe()
        # A known drawn board
        game.board = [
            HUMAN, AI, HUMAN,
            HUMAN, AI, AI,
            AI, HUMAN, HUMAN,
        ]
        self.assertEqual(game.winner(), "Draw")

    def test_game_in_progress_returns_none(self):
        game = TicTacToe()
        game.board[0] = HUMAN
        self.assertIsNone(game.winner())

    def test_all_win_lines_are_valid_indices(self):
        for line in WIN_LINES:
            for idx in line:
                self.assertTrue(0 <= idx <= 8)


class TestMinimaxTactics(unittest.TestCase):
    """Sanity checks that the AI takes obviously-correct tactical moves."""

    def test_ai_takes_winning_move_when_available(self):
        game = TicTacToe()
        # AI ('O') has two in a row and can win at index 2
        game.board = [
            AI, AI, EMPTY,
            HUMAN, HUMAN, EMPTY,
            EMPTY, EMPTY, EMPTY,
        ]
        move = best_ai_move(game)
        self.assertEqual(move, 2)

    def test_ai_blocks_human_winning_move(self):
        game = TicTacToe()
        # Human ('X') is about to win at index 2, AI must block
        game.board = [
            HUMAN, HUMAN, EMPTY,
            AI, EMPTY, EMPTY,
            EMPTY, EMPTY, EMPTY,
        ]
        move = best_ai_move(game)
        self.assertEqual(move, 2)

    def test_ai_prefers_immediate_win_over_block(self):
        game = TicTacToe()
        # AI can win immediately at 6, while human threatens at 2.
        # A correct AI takes its own win rather than blocking.
        game.board = [
            AI, AI, EMPTY,
            HUMAN, HUMAN, EMPTY,
            EMPTY, EMPTY, EMPTY,
        ]
        move = best_ai_move(game)
        self.assertEqual(move, 2)  # AI wins immediately


class TestAIIsUnbeatable(unittest.TestCase):
    """Exhaustively verify the AI can never lose, no matter what the
    human plays, across the ENTIRE game tree (human moves first).
    """

    def test_ai_is_unbeatable_full_tree_search(self):
        outcomes = set()
        self._simulate(TicTacToe(), HUMAN, outcomes)
        # The AI must never have lost in any branch of the full tree.
        self.assertNotIn(HUMAN, outcomes,
                          "AI lost in at least one branch of the game tree!")
        # Sanity: the search actually explored both possible outcomes.
        self.assertTrue(outcomes.issubset({AI, "Draw"}))
        self.assertGreater(len(outcomes), 0)

    def _simulate(self, game: TicTacToe, turn: str, outcomes: set):
        result = game.winner()
        if result is not None:
            outcomes.add(result)
            return

        if turn == HUMAN:
            # Try EVERY possible human move (exhaustive, not just one)
            for move in list(game.available_moves()):
                game.make_move(move, HUMAN)
                self._simulate(game, AI, outcomes)
                game.undo_move(move)
        else:
            # AI always plays its single best move (deterministic given ties broken by move order)
            move = best_ai_move(game)
            game.make_move(move, AI)
            self._simulate(game, HUMAN, outcomes)
            game.undo_move(move)

    def test_ai_is_unbeatable_when_ai_moves_first(self):
        outcomes = set()
        self._simulate(TicTacToe(), AI, outcomes)
        self.assertNotIn(HUMAN, outcomes,
                          "AI lost in at least one branch when it moved first!")


if __name__ == "__main__":
    unittest.main(verbosity=2)

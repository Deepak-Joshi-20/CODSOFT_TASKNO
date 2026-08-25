"""
CODSOFT_TASKSNO - Task 2: Tic-Tac-Toe AI
Author: Deepak Joshi (0251CYS023)

An unbeatable Tic-Tac-Toe AI built with the Minimax algorithm plus
Alpha-Beta pruning (for speed - functionally identical result to
plain Minimax, just faster since the game tree is fully searched
either way for this small board).

The human plays 'X', the AI plays 'O'. The AI can never lose - the
best a human can achieve is a draw.

Concepts demonstrated:
    - Game tree search (Minimax)
    - Alpha-Beta pruning
    - Terminal-state evaluation
    - Simple text-based UI + input validation
"""

import math
from typing import List, Optional, Tuple

HUMAN = "X"
AI = "O"
EMPTY = " "

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


class TicTacToe:
    def __init__(self):
        self.board: List[str] = [EMPTY] * 9

    # ------------------------------------------------------------------
    # Board utilities
    # ------------------------------------------------------------------
    def available_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def make_move(self, index: int, player: str) -> bool:
        if self.board[index] == EMPTY:
            self.board[index] = player
            return True
        return False

    def undo_move(self, index: int) -> None:
        self.board[index] = EMPTY

    def winner(self) -> Optional[str]:
        """Return 'X', 'O', 'Draw', or None (game still in progress)."""
        for a, b, c in WIN_LINES:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if EMPTY not in self.board:
            return "Draw"
        return None

    def is_game_over(self) -> bool:
        return self.winner() is not None

    def print_board(self) -> None:
        symbols = [c if c != EMPTY else str(i) for i, c in enumerate(self.board)]
        rows = [symbols[0:3], symbols[3:6], symbols[6:9]]
        print()
        for r_idx, row in enumerate(rows):
            print(f" {row[0]} | {row[1]} | {row[2]} ")
            if r_idx < 2:
                print("---+---+---")
        print()


# ------------------------------------------------------------------
# Minimax with Alpha-Beta pruning
# ------------------------------------------------------------------
def minimax(game: TicTacToe, depth: int, is_maximizing: bool,
            alpha: float, beta: float) -> int:
    """Returns a score for the current board from AI's perspective:
       +10 - depth  -> AI wins (prefer faster wins)
       -10 + depth  -> Human wins (prefer slower losses)
        0            -> Draw
    """
    result = game.winner()
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in game.available_moves():
            game.make_move(move, AI)
            score = minimax(game, depth + 1, False, alpha, beta)
            game.undo_move(move)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # prune
        return best_score
    else:
        best_score = math.inf
        for move in game.available_moves():
            game.make_move(move, HUMAN)
            score = minimax(game, depth + 1, True, alpha, beta)
            game.undo_move(move)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # prune
        return best_score


def best_ai_move(game: TicTacToe) -> int:
    """Search all available moves and return the index of the best one
    for the AI, using Minimax + Alpha-Beta pruning.
    """
    best_score = -math.inf
    best_move = -1
    for move in game.available_moves():
        game.make_move(move, AI)
        score = minimax(game, 0, False, -math.inf, math.inf)
        game.undo_move(move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# ------------------------------------------------------------------
# CLI game loop
# ------------------------------------------------------------------
def get_human_move(game: TicTacToe) -> int:
    while True:
        raw = input(f"Your move ({HUMAN}) - enter a number 0-8: ").strip()
        if not raw.isdigit():
            print("Please enter a valid number between 0 and 8.")
            continue
        move = int(raw)
        if move < 0 or move > 8:
            print("Number must be between 0 and 8.")
            continue
        if move not in game.available_moves():
            print("That cell is already taken. Choose another.")
            continue
        return move


def play():
    game = TicTacToe()
    print("Tic-Tac-Toe: You are 'X', the AI is 'O'.")
    print("Cell positions are numbered like this:")
    print(" 0 | 1 | 2 \n---+---+---\n 3 | 4 | 5 \n---+---+---\n 6 | 7 | 8 \n")

    current_player = HUMAN  # human moves first
    game.print_board()

    while not game.is_game_over():
        if current_player == HUMAN:
            move = get_human_move(game)
            game.make_move(move, HUMAN)
        else:
            print("AI is thinking...")
            move = best_ai_move(game)
            game.make_move(move, AI)
            print(f"AI plays at position {move}.")

        game.print_board()
        current_player = AI if current_player == HUMAN else HUMAN

    result = game.winner()
    if result == "Draw":
        print("It's a draw! Nobody wins.")
    elif result == AI:
        print("The AI wins! Better luck next time.")
    else:
        print("Congratulations, you won! (Shouldn't be possible against a perfect AI \U0001F600)")


if __name__ == "__main__":
    play()

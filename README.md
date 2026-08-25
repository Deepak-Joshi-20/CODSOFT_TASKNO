# Task 2 — Tic-Tac-Toe AI

An unbeatable Tic-Tac-Toe AI powered by the **Minimax algorithm with
Alpha-Beta pruning**. You are `X`, the AI is `O`.

## How it works
- `minimax()` recursively scores every possible continuation of the game:
  `+10 - depth` if the AI wins, `depth - 10` if you win, `0` for a draw.
  Subtracting/adding `depth` makes the AI prefer winning **sooner** and
  losing **later** (delays the inevitable if it's ever in a bad spot).
- Alpha-Beta pruning cuts off branches that can't affect the final
  decision, making the search faster without changing the result.
- `best_ai_move()` tries every legal move, runs `minimax()` on each, and
  picks the one with the highest score.

## Run it
```bash
python3 tictactoe.py
```
Enter a number 0-8 corresponding to the board position shown at the start.

## Run the tests
```bash
python3 -m unittest test_tictactoe.py -v
```
16/16 tests passing. The key test, `test_ai_is_unbeatable_full_tree_search`,
**exhaustively plays out every possible game** (the human tries every legal
move at every turn, branching the full game tree) and asserts the human
never wins in any branch — a mathematical proof of unbeatability, not just
a spot-check.

## Example
```
 0 | 1 | 2 
---+---+---
 3 | 4 | 5 
---+---+---
 6 | 7 | 8 

Your move (X) - enter a number 0-8: 0
AI is thinking...
AI plays at position 4.
...
```

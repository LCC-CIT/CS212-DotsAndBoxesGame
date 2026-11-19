"""Test driver for the GameLogic class. Run it with: python test_game_logic.py"""
from grid import Grid
from player import Player
from game_logic import GameLogic


def check(description, actual, expected):
    """Print PASS if actual equals expected, otherwise print FAIL and both values."""
    if actual == expected:
        print(f"PASS: {description}")
    else:
        print(f"FAIL: {description} (expected {expected}, got {actual})")


grid = Grid(3)  # 3x3 dots, so 2x2 boxes
alice = Player("Alice")
bob = Player("Bob")
game_logic = GameLogic(grid, [alice, bob])

check("A 3x3 board starts with 12 legal moves", len(game_logic.get_valid_moves()), 12)

# Draw three sides of the top-left box. None of them should complete it.
grid.add_line((0, 0), (1, 0))  # top
grid.add_line((0, 0), (0, 1))  # left
grid.add_line((1, 0), (1, 1))  # right
check("Three sides don't complete a box", game_logic.check_for_squares((1, 0), (1, 1)), 0)

# Draw the fourth side.
grid.add_line((0, 1), (1, 1))  # bottom
check("The fourth side completes one box", game_logic.check_for_squares((0, 1), (1, 1)), 1)
check("The completed box is at 0,0", game_logic.completed_squares, {(0, 0)})
check("8 legal moves are left", len(game_logic.get_valid_moves()), 8)

alice.add_score(1)
check("Alice has 1 point", alice.score, 1)

check("Alice goes first", game_logic.get_current_player(), alice)
game_logic.switch_player()
check("Bob goes next", game_logic.get_current_player(), bob)

check("The game isn't over yet", game_logic.is_game_over(), False)

print("\nThe grid should show the top-left box marked with an X:")
grid.display(game_logic.completed_squares)

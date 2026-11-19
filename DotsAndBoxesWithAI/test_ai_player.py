"""Test driver for the AI player. Run it with: python test_ai_player.py

Part 1 tests the code that builds the prompt and reads the reply. It doesn't call the model.
Part 2 asks the model for a real move, so it needs an OpenRouter API key in .env.
"""
from grid import Grid
from player import Player
from game_logic import GameLogic
from ai_player import AIPlayer, build_prompt, parse_move


def check(description, actual, expected):
    """Print PASS if actual equals expected, otherwise print FAIL and both values."""
    if actual == expected:
        print(f"PASS: {description}")
    else:
        print(f"FAIL: {description} (expected {expected}, got {actual})")


print("Part 1: Building the prompt and reading the reply (no model call)\n")

check("Read a reply that is just a move", parse_move("0,0 1,0"), ((0, 0), (1, 0)))
check("Read a move with extra text around it", parse_move("I'll play 1,1 1,2."), ((1, 1), (1, 2)))
check("Reply with no move in it", parse_move("I'm not sure."), None)

grid = Grid(3)
grid.add_line((0, 0), (1, 0))
game_logic = GameLogic(grid, [AIPlayer("AI"), Player("Human")])
prompt = build_prompt(grid, game_logic.get_valid_moves())
check("The prompt lists the line already drawn", "Lines already drawn: 0,0 1,0" in prompt, True)
legal_moves_part = prompt.split("Legal moves:")[1]
check("The drawn line isn't listed as a legal move", "0,0 1,0" in legal_moves_part, False)

print("\nThis is the prompt the model gets:")
print(prompt)

print("\nPart 2: Asking the model for a move\n")

ai = game_logic.players[0]
try:
    move = ai.choose_move(game_logic)
    print(f"The model chose: {move}")
    check("The model's move is legal", grid.is_valid_line(move[0], move[1]), True)
except Exception as error:
    print(f"FAIL: The model didn't give a move: {error}")

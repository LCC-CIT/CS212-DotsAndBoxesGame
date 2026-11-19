"""An AI player that asks an LLM which line to draw."""
import re

from player import Player
from llm_client import ask_llm

SYSTEM_PROMPT = (
    "You are an AI opponent in the game Dots and Boxes. "
    "Reply with ONLY one legal move in the format x1,y1 x2,y2 and nothing else. "
    "Prefer moves that complete a box. Avoid drawing the third side of a box, "
    "because that lets your opponent complete it."
)


def format_move(move):
    """Turn ((x1, y1), (x2, y2)) into the text 'x1,y1 x2,y2'."""
    (x1, y1), (x2, y2) = move
    return f"{x1},{y1} {x2},{y2}"


def build_prompt(grid, valid_moves):
    """Describe the board to the model."""
    lines_drawn = "; ".join(format_move(line) for line in grid.lines)
    legal_moves = "; ".join(format_move(move) for move in valid_moves)
    return (
        f"The board has {grid.size}x{grid.size} dots, numbered from 0,0 (top left) "
        f"to {grid.size - 1},{grid.size - 1} (bottom right).\n"
        f"Lines already drawn: {lines_drawn or 'none'}\n"
        f"Legal moves: {legal_moves}\n"
        "Which line do you draw?"
    )


def parse_move(reply):
    """Find the first 'x1,y1 x2,y2' in the model's reply.

    Returns ((x1, y1), (x2, y2)), or None if the reply has no move in it.
    """
    match = re.search(r"(\d+),(\d+)\s+(\d+),(\d+)", reply)
    if match is None:
        return None
    x1, y1, x2, y2 = map(int, match.groups())
    return (x1, y1), (x2, y2)


class AIPlayer(Player):
    def choose_move(self, game_logic):
        """Ask the model for a move. Raises an error if it doesn't give a legal one."""
        grid = game_logic.grid
        prompt = build_prompt(grid, game_logic.get_valid_moves())
        reply = ask_llm(SYSTEM_PROMPT, prompt)

        move = parse_move(reply)
        if move is None or not grid.is_valid_line(move[0], move[1]):
            raise ValueError(f"The model did not give a legal move. It replied: {reply!r}")
        return move

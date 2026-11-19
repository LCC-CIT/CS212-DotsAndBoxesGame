import re
from pathlib import Path

try:
    from dotenv import dotenv_values
    from openai import OpenAI
except ImportError:  # Dependencies not installed yet
    dotenv_values = None  # type: ignore
    OpenAI = None  # type: ignore

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "baidu/ernie-5.5-flash-preview:free"

# Read the settings in the .env file next to this module (works from any cwd)
ENV_FILE = Path(__file__).with_name(".env")

SYSTEM_PROMPT = (
    "You are an AI opponent for the Dots and Boxes game. "
    "Return ONLY one legal move in the format: x1,y1 x2,y2. "
    "Do not include explanations unless they start with '#'. "
    "Prefer moves that complete squares; avoid giving the opponent easy squares."
)

MOVE_REGEX = re.compile(r"(\d+),(\d+)\s+(\d+),(\d+)")


def _build_dynamic_prompt(board_size: int,
                           lines_drawn,
                           completed_squares,
                           player_scores,
                           current_player: str,
                           valid_moves) -> str:
    # Truncate valid moves list if very large to reduce token usage
    max_show = 60
    vm_strs = [f"{a[0]},{a[1]} {b[0]},{b[1]}" for (a, b) in valid_moves[:max_show]]
    truncated = len(valid_moves) > max_show
    lines_str = [f"{a[0]},{a[1]} {b[0]},{b[1]}" for (a, b) in lines_drawn]
    squares_str = [f"{x},{y}" for (x, y) in completed_squares]
    scores_parts = [f"{name}:{score}" for name, score in player_scores.items()]
    prompt = [
        f"BOARD_SIZE: {board_size}",
        f"LINES_DRAWN_COUNT: {len(lines_drawn)}",
        f"LINES_DRAWN: [{'; '.join(lines_str)}]",
        f"COMPLETED_SQUARES_COUNT: {len(completed_squares)}",
        f"COMPLETED_SQUARES: [{'; '.join(squares_str)}]",
        f"PLAYER_SCORES: [{'; '.join(scores_parts)}]",
        f"CURRENT_PLAYER: {current_player}",
        f"VALID_MOVES_COUNT: {len(valid_moves)}",
        f"VALID_MOVES: [{'; '.join(vm_strs)}]",
    ]
    if truncated:
        prompt.append("VALID_MOVES_TRUNCATED: true")
    prompt.append("RETURN: one move in format 'x1,y1 x2,y2'")
    return "\n".join(prompt)


def request_move(board_size: int,
                 lines_drawn,
                 completed_squares,
                 player_scores,
                 current_player: str,
                 valid_moves):
    """Ask an OpenRouter model for a move. Returns (start,end) or None if unavailable."""
    if OpenAI is None or dotenv_values is None:
        return None  # Dependencies missing: caller picks a random move
    api_key = dotenv_values(ENV_FILE).get("OPENROUTER_API_KEY")
    if not api_key:
        return None  # No key: caller picks a random move

    try:
        client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
        dynamic_prompt = _build_dynamic_prompt(board_size, lines_drawn, completed_squares,
                                               player_scores, current_player, valid_moves)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": dynamic_prompt},
            ],
        )
        text = (response.choices[0].message.content or "").strip()
        match = MOVE_REGEX.search(text)
        if not match:
            return None
        x1, y1, x2, y2 = map(int, match.groups())
        start = (x1, y1)
        end = (x2, y2)
        # Basic adjacency validation; full validation happens in caller
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return None
        return start, end
    except Exception:
        return None

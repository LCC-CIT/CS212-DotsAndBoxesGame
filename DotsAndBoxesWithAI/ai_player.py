import random
from player import Player
from llm_client import request_move

class AIPlayer(Player):
    """AI Player that asks an OpenRouter LLM for its moves."""

    def choose_move(self, game_logic):
        valid_moves = game_logic.get_valid_moves()
        if not valid_moves:
            return None
        # Attempt LLM move via OpenRouter
        player_scores = {p.name: p.score for p in game_logic.players}
        lines_drawn = list(game_logic.grid.lines)
        completed_squares = list(game_logic.completed_squares)
        move = request_move(
            board_size=game_logic.grid.size,
            lines_drawn=lines_drawn,
            completed_squares=completed_squares,
            player_scores=player_scores,
            current_player=self.name,
            valid_moves=valid_moves,
        )
        if move and move in valid_moves:
            return move
        # The model failed or gave an illegal move: pick any legal move instead
        return random.choice(valid_moves)

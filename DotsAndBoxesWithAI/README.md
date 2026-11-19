# Dots and Boxes Game

A command-line implementation of the classic Dots and Boxes game in Python.

## Game Overview

Dots and Boxes is a pencil-and-paper game for two or more players. Players take turns connecting dots on a grid to form lines. When a player completes the fourth side of a square, they score a point and get another turn. The game ends when all squares are completed, and the player with the most squares wins!

## Project Structure

```
DotsAndBoxes/
├── grid.py           # Grid and line management
├── player.py         # Player representation
├── game_logic.py     # Game rules and square detection
├── ui.py             # User interface
├── ai_player.py      # AI player (asks the LLM for moves)
├── llm_client.py     # OpenRouter chat-completions client
├── main.py           # Game entry point
├── test.py           # Unit tests for grid module
└── test_game.py      # Integration tests for game logic
```

## Module Descriptions

### `grid.py`
- Manages the grid of dots and lines
- Validates line placement (adjacency, bounds checking)
- Displays the current grid state with completed squares marked

### `player.py`
- Represents a player with a name and score
- Handles score updates

### `game_logic.py`
- Implements game rules
- Detects completed squares when lines are added
- Manages player turns
- Determines when the game is over and who wins

### `ui.py`
- Provides the command-line interface
- Displays the grid, scores, and game status
- Handles user input for drawing lines

### `main.py`
- Entry point for the game
- Initializes all components
- Runs the main game loop

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. Set up the game:
   - Enter the grid size (e.g., 4 for a 4x4 grid)
   - Enter the number of players (2-4)
   - Enter names for each player

3. Take turns:
   - Players enter coordinates to draw a line between two adjacent dots
   - Format: `x1,y1 x2,y2` (e.g., `0,0 0,1`)
   - If you complete a square, you get another turn!

4. Win the game:
   - The game ends when all squares are completed
   - The player with the most squares wins!

## Example Gameplay

```
Enter grid size (e.g., 4 for 4x4): 3
Enter number of players (2-4): 2
Enter name for Player 1: Alice
Enter name for Player 2: Bob

==================================================

o   o   o
         
o   o   o
         
o   o   o
==================================================

Scores:
  Alice: 0 points
  Bob: 0 points

Alice's turn!

Enter coordinates to draw a line between two adjacent dots.
Format: x1,y1 x2,y2 (e.g., '0,0 0,1')
Your move: 0,0 1,0

[Line added... continue playing...]
```

## Running Tests

### Unit Tests (Grid Module)
```bash
python test.py
```

### Integration Tests (Game Logic)
```bash
python test_game.py
```

### Run All Tests
```bash
python -m unittest discover
```

## Features

- ✅ Dynamic grid size (2x2 to any size)
- ✅ Support for 2-4 players
- ✅ Automatic square detection
- ✅ Extra turns when completing squares
- ✅ Visual display of completed squares (marked with 'X')
- ✅ Score tracking
- ✅ Input validation
- ✅ Winner determination
- ✅ Optional AI opponent (OpenRouter LLM)

## Requirements

- Python 3.7 or higher
- Optional: the LLM AI opponent requires the packages in `requirements.txt` and an OpenRouter API key in `.env`.

## Game Rules

1. Players take turns drawing one line at a time
2. Lines must connect two adjacent dots (horizontally or vertically)
3. When a player completes the fourth side of a square, they:
   - Score one point
   - Get to take another turn
4. The game continues until all squares are completed
5. The player with the most squares wins
6. If tied, the game ends in a draw

## Tips for Playing

- Try to force your opponent into giving you squares
- Be careful not to give your opponent the third side of a square
- Plan ahead to create chains of squares
- The endgame often involves sacrificing squares to set up larger chains

## Game State Representation
Grid.size + Grid.lines → board geometry
GameLogic.completed_squares (which boxes are done; you may also want a mapping to the claiming player)
GameLogic.current_player_index and players (with scores)

## AI Opponent (Optional)
You can add an AI player when configuring players by typing `AI` for the player type.

### How It Chooses Moves
1. Asks an LLM on [OpenRouter](https://openrouter.ai) for a move (if an API key is in `.env` and the dependencies are installed).
2. If the model is unavailable or its move is not legal, the AI picks a random legal move.

The model is set by `MODEL` in `llm_client.py` (default: `baidu/ernie-5.5-flash-preview:free`). Any OpenRouter model ID will work.

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Setting the API Key
1. Get an API key from https://openrouter.ai/keys.
2. Copy `.env.example` to `.env` in this folder.
3. Put your key in `.env`:
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   ```

`.env` is listed in `.gitignore`, so your key will not be committed. Never commit a real key.

### Dynamic Prompt Contents Sent to the Model
- Board size
- Current lines
- Completed squares
- Player scores
- Current player name
- Valid moves list (may truncate if large)

### Expected Model Output
Return exactly: `x1,y1 x2,y2` (e.g., `0,0 0,1`). Any other format makes the AI pick a random legal move.

### Offline / No Key
If the key or dependencies are missing, the AI still plays, using random legal moves.

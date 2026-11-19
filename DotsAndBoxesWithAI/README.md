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
├── ai_player.py      # AI player: builds the prompt and reads the model's move
├── llm_client.py     # Sends a prompt to a model on OpenRouter
├── main.py           # Game entry point
├── test_grid.py      # Test driver for grid.py
├── test_game_logic.py  # Test driver for game_logic.py
└── test_ai_player.py # Test driver for ai_player.py (part 2 calls the model)
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

## Running the Test Drivers

Each test driver runs some code and prints `PASS` or `FAIL` for each check.

```bash
python test_grid.py
python test_game_logic.py
python test_ai_player.py
```

Part 2 of `test_ai_player.py` asks the model for a real move, so it needs your API key in `.env`.

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
1. `ai_player.py` describes the board in a prompt, and `llm_client.py` sends it to a model on [OpenRouter](https://openrouter.ai).
2. If the model isn't responding, its reply has no move, or the move is illegal, the game shows an error message and ends.

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

### What the Prompt Contains
- Board size
- Lines already drawn
- Legal moves

### Expected Model Output
One move in the format `x1,y1 x2,y2` (e.g., `0,0 0,1`). The game uses the first move it finds in the reply. If there's no move in the reply, that's an error.

### Offline / No Key
If the key or the packages are missing, or OpenRouter can't be reached, the game shows an error message on the AI's turn and ends. Games with only human players don't need a key, but the packages still need to be installed.

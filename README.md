# CS212-DotsAndBoxesGame

Example console implementations of the Dots and Boxes game in Python, used in Lane CC CS212: AI Programming 1.

Course materials: https://github.com/LCC-CIT/CS212-CourseMaterials/

More CS212 examples: https://github.com/LCC-CIT/CS212-Examples

## Projects

- [DotsAndBoxes](DotsAndBoxes/)
  - A two-player console game built around a `GameBoard` class (game logic) and a separate console UI. It uses only the Python standard library.
  - Includes a step-by-step [tutorial](DotsAndBoxes/tutorial/) covering the game overview, game logic, console UI, and AI integration.
  - Run it with `python dots_and_boxes.py`. See its [README](DotsAndBoxes/README.md) for details.

- [DotsAndBoxesWithAI](DotsAndBoxesWithAI/)
  - A different implementation with a configurable grid size, 2–4 players, simple test drivers, and an optional AI opponent.
  - The AI player asks an LLM on OpenRouter for a move (using the OpenAI Python SDK) when the packages in `requirements.txt` are installed and `OPENROUTER_API_KEY` is set in a `.env` file. If the model isn't responding or gives an illegal move, the game shows an error message and ends.
  - Run it with `python main.py`. See its [README](DotsAndBoxesWithAI/README.md) for details.

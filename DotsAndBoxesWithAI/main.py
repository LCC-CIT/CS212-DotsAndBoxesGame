from grid import Grid
from player import Player
from ai_player import AIPlayer, format_move
from game_logic import GameLogic
from ui import UI


def main():
    """
    Main function to run the Dots and Boxes game.
    """
    # Get game setup from user
    try:
        grid_size = int(input("\nEnter grid size (e.g., 4 for 4x4): "))
        if grid_size < 2:
            print("Grid size must be at least 2. Setting to 4.")
            grid_size = 4
    except ValueError:
        print("Invalid input. Using default size of 4.")
        grid_size = 4

    try:
        num_players = int(input("Enter number of players (2-4): "))
        if num_players < 2 or num_players > 4:
            print("Number of players must be between 2 and 4. Setting to 2.")
            num_players = 2
    except ValueError:
        print("Invalid input. Using 2 players.")
        num_players = 2

    # Create players (human or AI)
    players = []
    print("\nConfigure players:")
    for i in range(num_players):
        name = input(f"Enter name for Player {i + 1}: ").strip()
        if not name:
            name = f"Player {i + 1}"
        ptype = input("  Type 'AI' for AI player, anything else for Human: ").strip().lower()
        if ptype == 'ai':
            players.append(AIPlayer(name))
        else:
            players.append(Player(name))

    # Initialize game components
    grid = Grid(grid_size)
    game_logic = GameLogic(grid, players)
    ui = UI(grid, game_logic)

    # Display welcome and instructions
    ui.display_welcome()

    # Main game loop
    while not game_logic.is_game_over():
        ui.display_grid()
        ui.display_scores()
        ui.display_current_player()

        current = game_logic.get_current_player()
        if isinstance(current, AIPlayer):
            # Ask the LLM for a move. Stop the game if it can't give one.
            try:
                start, end = current.choose_move(game_logic)
            except Exception as error:
                print(f"\nAI error: {error}")
                print("The game cannot continue without the AI. Goodbye!")
                return
            print(f"{current.name} (AI) plays: {format_move((start, end))}")
        else:
            # Human input
            line_coords = ui.get_line_input()
            if line_coords is None:
                continue
            start, end = line_coords

        # Try to add line for either player type
        if grid.add_line(start, end):
            squares_completed = game_logic.check_for_squares(start, end)
            if squares_completed > 0:
                print(f"\n🎊 {current.name} completed {squares_completed} square(s)!")
                current.add_score(squares_completed)
                print("You get another turn!")
            else:
                game_logic.switch_player()
        else:
            print("\n❌ Invalid move! That line is either already drawn, not adjacent, or out of bounds.")
            print("Try again.")

    # Game over - display results
    ui.display_grid()
    ui.display_winner()


if __name__ == "__main__":
    main()

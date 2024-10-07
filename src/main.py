"""
Main Class
--------------
Represents main entry point of the Breakout game.
"""

from breakout_game import BreakoutGame

def main():
    """
    This function initializes the BreakoutGame instance and starts the game loop.
    It serves as the starting point when the script is executed directly.
    """
    game = BreakoutGame() # Create an instance of the BreakoutGame class
    game.run() # Start the game loop

if __name__ == "__main__":
    # Ensure that the main() function is called only when this script is executed directly,
    # not when it is imported as a module in another script.
    main()

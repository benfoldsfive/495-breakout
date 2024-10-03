# Breakout 2K25

Welcome to Breakout 2K25, a classic arcade-style brick-breaking game built using Python and Pygame.
Control a paddle to bounce a ball and break all the bricks on the screen.
This game includes multiple enhancements to the original Atari arcade game Breakout, including power-ups, special effects, and an authentication system for players to save high scores.

#  Features

Power-ups: Special bricks drop power-ups, such as increasing paddle size, slowing down the ball, or granting extra lives.

Visual Effects: Particles and fragments appear when bricks are broken. A trail of fire follows the ball wherever it goes. Falling stars decorate the background.

User Authentication: Players can log in or register to track their scores.

Background Music & Sounds: Retro music and sound effects create a lively, nostalgic atmosphere.

Multiple Levels: Each new level brings more challenging brick layouts and speed.

# Installation Instructions

Prerequisites: Python 3.7+, 
Pygame library (pygame 2.0+)

1) Download the Repository - Clone the repository or download the source code zip and extract it
2) Install Required Dependencies - Run the following command to install the required libraries:
bash
Copy code
pip install pygame
3) Run the Game - Execute the main.py file:
bash
Copy code
python main.py

# Controls

Arrow Keys: Move the paddle left or right.
P: Pause the game.
Enter: Resume the game or start a new level after login.
R: Restart the game when game over.
Game States

Main Menu: Log in or register to start the game.
Post-Login Menu: Start the game after login.
Game Running: Normal gameplay.
Paused: Pauses the game.
Game Over: Restart the game or exit.

# Power-Ups

Power-ups are dropped by special bricks and offer the following benefits:

1) Increase Paddle Size: Expands the paddle width temporarily
2) Slow Ball: Reduces the ball's speed
3) Extra Life: Grants one additional life

# How to Play

Launch the game on main.py and log in or register.
Control the paddle with the arrow keys to prevent the ball from falling.
Break all the bricks on the screen to proceed to the next level.
Collect power-ups by catching them with the paddle.
Try to achieve a high score by progressing through levels without losing all lives.

# Saving and High Scores

Each player’s high score is saved after each game and can be viewed after logging in.
Scores are updated at the end of each game session.

# License

This project is open-source and available under the MIT License.

Enjoy the game! 🎮
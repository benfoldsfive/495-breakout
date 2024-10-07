"""
Power Up Class
--------------
Represents a power-up in a game.

This class handles the creation, drawing, movement, and activation of different types
of power-ups that the player can collect during the game. The power-up type dictates
what effect it will have once activated (ex. increase paddle size, slow ball, extra life).
"""

import pygame


class PowerUp:
    def __init__(self, x, y, power_up_type):
        """
        Initializes the PowerUp object with position and type.

        Arguments:
            - x: The initial x-coordinate of the power-up.
            - y: The initial y-coordinate of the power-up.
            - power_up_type: The type of the power-up (e.g., "increase_paddle_size", "slow_ball", "extra_life").

        This method sets up the power-up's position, its type, and its rectangular area.
        """
        self.x = x  # X position of the power-up
        self.y = y  # Y position of the power-up
        self.power_up_type = power_up_type  # Type of the power-up effect
        self.rect = pygame.Rect(self.x, self.y, 20, 20)   # Rectangle representing the power-up's size and position

    def draw(self, screen, power_up_type):
        """
        Draws the power-up on the screen based on its type.

        Arguments:
            - screen: The surface to draw the power-up on.
            - power_up_type: The type of power-up to be drawn. Changes the color based on type.

        This method draws the power-up using a colored rectangle. Each type of power-up is
        represented by a different color:
            - Green for "increase_paddle_size"
            - Blue for "slow_ball"
            - Red for "extra_life"
        """
        if power_up_type == "increase_paddle_size":
            pygame.draw.rect(screen, (0, 255, 0), self.rect) # Green for paddle size increase
        elif power_up_type == "slow_ball":
            pygame.draw.rect(screen, (0, 0, 255), self.rect) # Blue for ball slow down

        elif power_up_type == "extra_life":
            pygame.draw.rect(screen, (255, 0, 0), self.rect) # Red for extra life

    def move(self):
        """
        Moves the power-up downwards on the screen.

        This method controls the movement of the power-up, making it fall by increasing its
        y-coordinate. The power-up moves at a constant speed.
        """
        self.rect.y += 2 # Move the power-up down at a rate of 2 pixels per frame

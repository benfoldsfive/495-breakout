"""
Paddle Class
--------------
Represents the paddle in the Breakout game.
Handles the paddle's position, movement, and rendering on the screen.
"""
import pygame

# Paddle class
class Paddle:
    def __init__(self):
        """
        Initializes the Paddle instance.

        Sets the paddle's initial position and dimensions, centering it at the bottom of the game window.
        """
        self.rect = pygame.Rect(400 - 50, 580, 100, 10)  # Center the paddle

    def move(self, dx):
        """
        Moves the paddle horizontally.

        Arguments:
            - dx: The amount to move the paddle. Positive values move it right,
            while negative values move it left.

        This method ensures that the paddle does not move off the screen boundaries.
        """
        if 0 < self.rect.left + dx < 800 - 100:  # Check boundaries (0 to screen width minus paddle width)
            self.rect.move_ip(dx, 0) # Move the paddle by dx

    def draw(self, screen):
        """
        Draws the paddle on the specified screen.

        Arguments:
            - screen: The surface on which to draw the paddle.

        This method renders the paddle as a white rectangle on the game screen.
        """
        pygame.draw.rect(screen, (255, 255, 255), self.rect) # Draw the paddle as a white rectangle

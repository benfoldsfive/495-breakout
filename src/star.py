"""
Star Class
--------------
Represents a star in a starfield animation.

This class simulates a star's movement in a 2D space, giving the effect of a moving
starfield. Each star has a random position, size, and speed, creating a parallax-like
scrolling effect as stars move downward across the screen.
"""
import pygame
import random

class Star:
    def __init__(self):
        """
        Initializes a Star object with random position, size, and speed.

        This method generates random initial values for the star's:
            - x-coordinate (horizontal position)
            - y-coordinate (vertical position)
            - size (star radius, giving variation in star appearance)
            - speed (how fast the star moves, creating depth illusion)

        Stars are randomly distributed across the screen on initialization.
        """
        self.x = random.randint(0, 800) # Random x-coordinate within the screen width (800px)
        self.y = random.randint(0, 600) # Random y-coordinate within the screen height (600px)
        self.size = random.randint(1, 3)  # Random size of the star (1 to 3 pixels)
        self.speed = random.uniform(0.5, 2.0) # Random downward speed, creating varying depths

    def update(self):
        """
        Updates the position of the star, simulating movement.

        This method moves the star downward based on its speed. When a star goes off-screen,
        it resets its y-coordinate to the top (y = 0) and gives it a new random x-coordinate,
        simulating an infinite scrolling starfield.
        """
        self.y += self.speed # Move the star downward based on its speed
        if self.y > 600: # If the star moves off the bottom of the screen
            self.y = 0 # Reset the y-coordinate to the top
            self.x = random.randint(0, 800) # Randomly reposition the star along the x-axis


    def draw(self, screen):
        """
        Draws the star on the screen.

        Arguments:
            - screen: The surface where the star will be drawn.

        This method draws the star as a white circle at its current position
        (x, y) with its size determining the radius.
        """
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size) # Draw the star as a white circle

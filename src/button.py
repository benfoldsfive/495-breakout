"""
Button Class
--------------
Represents a clickable button in the game interface.
The button can change color when hovered over and can handle click events.
"""

import pygame

class Button:
    def __init__(self, x, y, w, h, text):
        """
        Initializes the Button instance at a specified position with given dimensions and text.

        Arguments:
            - x: The x-coordinate of the button's position.
            - y: The y-coordinate of the button's position.
            - w: The width of the button.
            - h: The height of the button.
            - text: The text label to display on the button.
        """
        self.rect = pygame.Rect(x, y, w, h) # Rectangle defining button boundaries
        self.color = pygame.Color('dodgerblue3') # Default button color
        self.text = text # Text to be displayed on the button
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, pygame.Color('white')) # Rendered text surface
        self.hovered = False # Flag to check if the button is hovered over

    def draw(self, screen):
        """
        Draws the button on the specified screen.

        Arguments:
            - screen: The surface on which to draw the button.
        """
        # Change color if the button is hovered
        self.color = pygame.Color('dodgerblue2') if self.hovered else pygame.Color('dodgerblue3')
        pygame.draw.rect(screen, self.color, self.rect) # Draw the button rectangle
        # Center the text on the button
        screen.blit(self.txt_surface, (self.rect.centerx - self.txt_surface.get_width() // 2,
                                       self.rect.centery - self.txt_surface.get_height() // 2))

    def handle_event(self, event):
        """
        Handles user input events for the button.

        Arguments:
            - event: The event to handle.

        Returns:
            - bool: True if the button was clicked, False otherwise.
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

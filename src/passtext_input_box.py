"""
Passtext Input Box Class
--------------
Represents a password input box with masked text input.

This class handles the display and interaction of a text input box for password
entry, where the input characters are masked (as '*'). The input box can be
activated by clicking and text can be entered, deleted, or reset.
"""

import pygame

class PassTextInputBox:
    def __init__(self, x, y, w, h, text=''):
        """
        Initializes the PassTextInputBox instance.

        Arguments:
            - x: X-coordinate of the input box.
            - y: Y-coordinate of the input box.
            - w: Width of the input box.
            - h: Height of the input box.
            - text: Initial text (default is an empty string).

        This constructor sets up the input box's rectangle, color, font, and masked text.
        The text is initially unmasked, but will be displayed as a series of '*' characters.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3') # Color when inactive
        self.text = text # Unmasked text
        self.masked_text = ''  # Masked version of the text
        self.font = pygame.font.Font(None, 36) # Font for rendering the text
        self.txt_surface = self.font.render(self.masked_text, True, self.color) # Text surface for rendering
        self.active = False # Track if the input box is clicked


    def handle_event(self, event):
        """
        Handles events for user input (e.g., mouse clicks and key presses).

        Arguments:
            - event: The event to handle (e.g., key press or mouse click).

        This method handles activating the input box on mouse clicks, updating the text
        when keys are pressed, and ensuring that the input is masked.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks inside the input box, toggle active state
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False # Deactivate if clicking outside
            # Change color based on active state
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                # Handle pressing Enter to submit text
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Can capture this input elsewhere
                    self.text = ''  # Reset after pressing Enter
                    self.masked_text = '' # Clear the masked text
                # Handle backspace to remove last character
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1] # Remove last character from raw text
                    self.masked_text = self.masked_text[:-1] # Remove last '*' from masked text
                # Handle normal text input (add character)
                else:
                    self.text += event.unicode # Add character to raw text
                    self.masked_text += '*'  # Append '*' for each character typed
                # Re-render the updated masked text
                self.txt_surface = self.font.render(self.masked_text, True, self.color)

    def draw(self, screen):
        """
        Draws the password input box and its contents on the screen.

        Arguments:
            - screen: The surface to draw on.

        This method renders the masked text inside the input box and draws the input
        box itself. It only displays the masked version of the text.
        """
        # Render the masked text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset(self):
        """
        Resets the input box by clearing both the raw and masked text.

        This method is used to reset the input box, clearing any entered text and
        resetting the display to show an empty field.
        """
        self.text = '' # Clear raw text
        self.masked_text = '' # Clear masked text
        self.txt_surface = self.font.render(self.masked_text, True, self.color) # Re-render empty masked text

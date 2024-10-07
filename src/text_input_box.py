"""
Text Input Box Class
--------------
Represents a text input box where users can type and submit text.

This class handles text input, allowing users to click to activate the box,
type characters, and press Enter to submit. The text can also be reset manually.
"""
import pygame

class TextInputBox:
    def __init__(self, x, y, w, h, text=''):
        """
        Initializes a TextInputBox with position, dimensions, and optional starting text.

        Arguments:
            - x: The x-coordinate of the input box.
            - y: The y-coordinate of the input box.
            - w: The width of the input box.
            - h: The height of the input box.
            - text: Optional initial text for the input box. Defaults to an empty string.
        """
        self.rect = pygame.Rect(x, y, w, h) # Create a rectangular area for the text input
        self.color = pygame.Color('lightskyblue3')  # Default color when the input box is inactive
        self.text = text    # Initial text
        self.font = pygame.font.Font(None, 36)  # Font for rendering the text
        self.txt_surface = self.font.render(text, True, self.color) # Rendered surface for the current text
        self.active = False # Track if the input box is clicked on

    def handle_event(self, event):
        """
        Handles events related to user interaction with the text input box.

        Arguments:
            - event: A pygame event, such as mouse click or keypress.

        Toggles the input box's active state on mouse click.
        Processes text input, such as adding characters, handling Enter key, and Backspace.
        Changes the input box's color when active or inactive.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks inside the input box, toggle active state
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # Change color based on whether the input box is active or inactive
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Submit the text
                    print(self.text)  # Can capture this input elsewhere
                    self.text = ''  # Reset after pressing Enter
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character when Backspace is pressed
                    self.text = self.text[:-1]
                else:
                    # Append the typed character to the input text
                    self.text += event.unicode
                # Re-render the text surface with the updated text
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        """
        Draws the input box and the current text on the screen.

        Arguments:
            - screen: The surface where the input box and text will be drawn.

        This method renders the current text inside the input box and draws a rectangle around it.
        """
        # Render the current text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Draw the rectangle outline of the input box
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset(self):
        """
        Resets the text input box, clearing any existing text.

        This method clears the input text and resets the rendered text surface.
        """
        self.text = '' # Clear the text
        self.txt_surface = self.font.render(self.text, True, self.color) # Re-render the text surface with the empty text

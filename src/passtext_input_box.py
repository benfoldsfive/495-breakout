# Password Input Box Field

import pygame

class PassTextInputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.masked_text = ''  # Masked version of the text
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(self.masked_text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks inside the input box, toggle active state
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Can capture this input elsewhere
                    self.text = ''  # Reset after pressing Enter
                    self.masked_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.masked_text = self.masked_text[:-1]
                else:
                    self.text += event.unicode
                    self.masked_text += '*'  # Append '*' for each character typed
                self.txt_surface = self.font.render(self.masked_text, True, self.color)

    def draw(self, screen):
        # Render the masked text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def reset(self):
        self.text = ''
        self.masked_text = ''
        self.txt_surface = self.font.render(self.masked_text, True, self.color)

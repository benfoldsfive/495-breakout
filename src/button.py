import pygame

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('dodgerblue3')
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, pygame.Color('white'))
        self.hovered = False

    def draw(self, screen):
        # Change color if the button is hovered
        self.color = pygame.Color('dodgerblue2') if self.hovered else pygame.Color('dodgerblue3')
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.centerx - self.txt_surface.get_width() // 2,
                                       self.rect.centery - self.txt_surface.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

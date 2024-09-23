import pygame

# Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(400 - 50, 580, 100, 10)  # Center the paddle

    def move(self, dx):
        if 0 < self.rect.left + dx < 800 - 100:
            self.rect.move_ip(dx, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

import pygame


class PowerUp:
    def __init__(self, x, y, power_up_type):
        self.x = x
        self.y = y
        self.power_up_type = power_up_type
        self.rect = pygame.Rect(self.x, self.y, 20, 20)  

    def draw(self, screen, power_up_type):
        if power_up_type == "increase_paddle_size":
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
        elif power_up_type == "slow_ball":
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
        elif power_up_type == "extra_life":
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def activate(self):
        print(f"Power-up activated: {self.power_up_type}")

    def move(self):
        self.rect.y += 2

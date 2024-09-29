import pygame
from particle import Particle

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(400 - 10, 300 - 10, 20, 20)  # Ball size and position
        self.dx, self.dy = 5, -5  # Ball speed in x and y direction
        self.trail = []  # To store the fire trail particles

    def move(self):
        # Create a fire particle at the ball's current position
        self.trail.append(Particle(self.rect.centerx, self.rect.centery))

        # Remove old particles from the trail to keep the length manageable
        if len(self.trail) > 20:  # Limit the trail to 20 particles
            self.trail.pop(0)

        # Move the ball by updating its position based on its velocity
        self.rect.move_ip(self.dx, self.dy)

    def check_collision_with_walls(self):
        # Reverse x direction if it hits left or right walls
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.dx = -self.dx
        # Reverse y direction if it hits the top
        if self.rect.top <= 0:
            self.dy = -self.dy

    def check_collision_with_paddle(self, paddle, particles):
        self.paddle_hit_sound = pygame.mixer.Sound("../sounds/hit_paddle.wav") # Load paddle hit sound
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy  # Bounce off the paddle
            pygame.mixer.Sound.play(self.paddle_hit_sound)  # Play paddle hit sound
            # Create fire particles on paddle hit
            for _ in range(10):
                particles.append(Particle(self.rect.centerx, self.rect.centery))

    def draw(self, screen):
        # Draw the fire trail effect
        for particle in self.trail:
            particle.update()  # Update each particle (movement, size, color)
            particle.draw(screen)  # Draw the particle to the screen

        # Draw the ball itself
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 10)

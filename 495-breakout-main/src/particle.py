import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x  # X position of the particle
        self.y = y  # Y position of the particle
        self.vx = random.uniform(-1.5, 1.5)  # Random horizontal velocity for curling effect
        self.vy = random.uniform(-2, 0)  # Random upward velocity for flame effect
        self.size = random.randint(5, 10)  # Random starting size of the particle
        self.lifetime = 50  # How long the particle will last
        
        # Vibrant initial color (randomized between orange, yellow, and red shades)
        self.color = (
            random.randint(200, 255),  # Red component
            random.randint(100, 200),  # Green component
            0  # Blue component (always 0 for fire)
        )

    def update(self):
        # Update particle position
        self.x += self.vx  # Apply horizontal velocity (curling effect)
        self.y += self.vy  # Apply vertical velocity (flame-like motion)

        # Gradually reduce size (simulate burning out)
        self.size -= 0.2
        self.size = max(self.size, 0)  # Ensure size doesn't go negative

        # Change color over time (from bright yellow -> orange -> red as it cools down)
        r, g, b = self.color
        r = min(255, r + 5)  # Increase red to make the core appear hotter
        g = max(0, g - 5)  # Decrease green to make the particle more red over time
        self.color = (r, g, 0)

        # Reduce particle lifetime
        self.lifetime -= 1

    def draw(self, screen):
        # Only draw the particle if it still has a positive size and lifetime
        if self.lifetime > 0 and self.size > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))


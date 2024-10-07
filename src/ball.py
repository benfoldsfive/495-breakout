"""
Ball Class
--------------
Controls the behavior and movement of the ball in the game.
Handles ball movement, collision with walls and paddle, and generates fire trail particles.
"""

import pygame
from pathlib import Path
from particle import Particle


current_dir = Path(__file__).parent.resolve() # Get the current directory
sounds_dir = current_dir.parent / "sounds" # Navigate to the sounds directory

class Ball:
    def __init__(self):
        """
        Initialize the Ball object with its initial position, speed, and particle trail.
        """
        self.rect = pygame.Rect(400 - 10, 300 - 10, 20, 20)  # Ball size and position
        self.dx, self.dy = 5, -5  # Ball speed in x and y direction
        self.trail = []  # To store the fire trail particles

    def move(self):
        """
        Move the ball according to its velocity and generate a fire trail.
        """
        # Create a fire particle at the ball's current position
        self.trail.append(Particle(self.rect.centerx, self.rect.centery))

        # Remove old particles from the trail to keep the length manageable
        if len(self.trail) > 20:  # Limit the trail to 20 particles
            self.trail.pop(0)

        # Move the ball by updating its position based on its velocity
        self.rect.move_ip(self.dx, self.dy)

    def check_collision_with_walls(self):
        """
        Check if the ball has collided with any walls and reverse direction if necessary.
        """
        # Reverse x direction if it hits left or right walls
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.dx = -self.dx
        # Reverse y direction if it hits the top
        if self.rect.top <= 0:
            self.dy = -self.dy

    def check_collision_with_paddle(self, paddle, particles):
        """
        Check for collisions with the paddle and handle the bounce and particle effects.
        Args:
            paddle: The paddle object the ball may collide with.
            particles: The list where new particles will be added on paddle hit.
        """
        paddle_hit_sound = pygame.mixer.Sound(sounds_dir / "hit_paddle.wav") # Load paddle hit sound using cross-platform paths
        if self.rect.colliderect(paddle.rect):
            self.dy = -self.dy  # Bounce off the paddle
            pygame.mixer.Sound.play(paddle_hit_sound)  # Play paddle hit sound
            # Create fire particles on paddle hit
            for _ in range(10):
                particles.append(Particle(self.rect.centerx, self.rect.centery))

    def draw(self, screen):
        """
        Draw the ball and its fire trail on the screen.
        Args:
            screen: The game screen to draw on.
        """
        # Draw the fire trail effect
        for particle in self.trail:
            particle.update()  # Update each particle (movement, size, color)
            particle.draw(screen)  # Draw the particle to the screen

        # Draw the ball itself
        pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 10)

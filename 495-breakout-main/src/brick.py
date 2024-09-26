import pygame
import random
import math

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 20)  # Standard brick dimensions
        self.frame_counter = 0  # To slow down the electric arc animation
        self.flicker_offset = 0  # Control flicker more subtly
        self.max_flicker_offset = 2  # Max amount for flickering movement
        self.flicker_direction = 1  # Flicker oscillates back and forth

    def draw(self, screen):
        # Update the frame counter for flicker effect
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:  # Reduce flicker frequency
            # Subtle flicker oscillation
            self.flicker_offset += self.flicker_direction
            if abs(self.flicker_offset) >= self.max_flicker_offset:
                self.flicker_direction *= -1  # Change direction

        # Draw the outer light red glow (with reduced flicker)
        outer_glow = pygame.Rect(
            self.rect.x - 6 + self.flicker_offset, self.rect.y - 6 + self.flicker_offset,
            self.rect.width + 12, self.rect.height + 12)
        pygame.draw.rect(screen, (255, 100, 100), outer_glow, border_radius=10)  # Lighter red

        # Draw the inner slightly darker red glow (with reduced flicker)
        inner_glow = pygame.Rect(
            self.rect.x - 3 + self.flicker_offset // 2, self.rect.y - 3 + self.flicker_offset // 2,
            self.rect.width + 6, self.rect.height + 6)
        pygame.draw.rect(screen, (255, 50, 50), inner_glow, border_radius=5)  # Darker red

        # Draw the actual red brick
        pygame.draw.rect(screen, (255, 0, 0), self.rect, border_radius=5)

        # Draw electric arcs around the brick
        self.draw_electric_arcs(screen)

    def draw_electric_arcs(self, screen):
        # Only update arcs every few frames for a smoother animation
        if self.frame_counter % 5 == 0:
            for _ in range(3):  # Fewer, smaller arcs
                start_angle = random.uniform(0, 2 * math.pi)
                end_angle = start_angle + random.uniform(0.2, 0.6)  # Short arc length
                radius = random.randint(10, 20)  # Small radius for arcs close to the brick

                # Random center positions near the brick for arcs
                center_x = self.rect.centerx + random.randint(-2, 2)
                center_y = self.rect.centery + random.randint(-2, 2)

                # Arc color (electric blue)
                arc_color = (random.randint(200, 255), random.randint(200, 255), 255)

                # Draw the arc close to the brick
                pygame.draw.arc(screen, arc_color, (center_x - radius, center_y - radius, radius * 2, radius * 2),
                                start_angle, end_angle, 2)

    def break_into_fragments(self):
        # Logic for breaking the brick into fragments
        fragment_width = random.uniform(self.rect.width // 4, self.rect.width // 2)
        fragment_height = random.uniform(self.rect.height // 4, self.rect.height // 2)
        fade_speed = random.uniform(0.05, 0.1)
        return BrickFragment(self.rect.x, self.rect.y, fragment_width, fragment_height, (255, 0, 0), fade_speed)


class BrickFragment:
    def __init__(self, x, y, width, height, color, fade_speed=0.05):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(1, 3)
        self.color = color
        self.fade_speed = fade_speed

    def update(self):
        # Update fragment position and shrink over time
        self.x += self.vx
        self.y += self.vy
        self.width -= self.fade_speed
        self.height -= self.fade_speed
        self.width = max(self.width, 0)
        self.height = max(self.height, 0)

    def draw(self, screen):
        # Draw the fragment if it's still visible
        if self.width > 0 and self.height > 0:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

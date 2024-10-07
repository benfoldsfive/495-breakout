"""
Brick Class
--------------
Represents a brick in the game, which can be drawn on the screen and can be broken into fragments.
The brick features a flickering effect to create a glowing appearance and emits electric arcs.
"""
import pygame
import random
import math

class Brick:
    def __init__(self, x, y):
        """
        Initializes the Brick instance at a specified (x, y) position.

        Arguments:
            - x: The x-coordinate of the brick's position.
            - y: The y-coordinate of the brick's position.
        """
        self.rect = pygame.Rect(x, y, 70, 20)  # Standard brick dimensions
        self.frame_counter = 0  # To slow down the electric arc animation
        self.flicker_offset = 0  # Control flicker more subtly
        self.max_flicker_offset = 2  # Max amount for flickering movement
        self.flicker_direction = 1  # Flicker oscillates back and forth
        self.power_up_type = None # Type of power-up associated with the brick

    def draw(self, screen):
        """
        Draws the brick on the specified screen with flicker and electric arc effects.

        Arguments:
            - screen: The surface on which to draw the brick.
        """
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
        """
        Draws electric arcs around the brick for a visual effect.
        The arcs are drawn at random positions near the brick to simulate electricity.

        Arguments:
            - screen: The surface on which to draw the electric arcs.
        """
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
        """
        Breaks the brick into smaller fragments when destroyed.

        Returns:
            - BrickFragment: An instance of BrickFragment representing a piece of the destroyed brick.
        """
        # Logic for breaking the brick into fragments
        fragment_width = random.uniform(self.rect.width // 4, self.rect.width // 2)
        fragment_height = random.uniform(self.rect.height // 4, self.rect.height // 2)
        fade_speed = random.uniform(0.05, 0.1) # Random fade speed for fragment
        return BrickFragment(self.rect.x, self.rect.y, fragment_width, fragment_height, (255, 0, 0), fade_speed)


class BrickFragment:
    """
    Represents a fragment of a broken brick, which moves and fades over time.
    The fragment has random velocities and a fade effect.
    """
    def __init__(self, x, y, width, height, color, fade_speed=0.05):
        """
        Initializes the BrickFragment instance at a specified (x, y) position with given dimensions.

        Arguments:
            - x: The x-coordinate of the fragment's position.
            - y: The y-coordinate of the fragment's position.
            - width: The initial width of the fragment.
            - height: The initial height of the fragment.
            - color: The RGB color of the fragment.
            - fade_speed: The rate at which the fragment fades over time.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = random.uniform(-1, 1) # Random horizontal velocity
        self.vy = random.uniform(1, 3) # Random vertical velocity
        self.color = color
        self.fade_speed = fade_speed

    def update(self):
        """
        Updates the position and size of the fragment over time.
        The fragment moves according to its velocity and shrinks based on the fade speed.
        The dimensions are clamped to a minimum of 0 to prevent negative sizes.
        """
        # Update fragment position and shrink over time
        self.x += self.vx
        self.y += self.vy
        self.width -= self.fade_speed
        self.height -= self.fade_speed
        self.width = max(self.width, 0) # Prevent negative width
        self.height = max(self.height, 0) # Prevent negative height

    def draw(self, screen):
        """
        Draws the fragment on the specified screen if it is still visible.

        Arguments:
            - screen (pygame.Surface): The surface on which to draw the fragment.
        """
        # Draw the fragment if it's still visible
        if self.width > 0 and self.height > 0:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

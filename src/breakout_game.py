import random

import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from particle import Particle
from power_up import PowerUp
from star import Star
from user_auth import load_users_from_file, register_user, login_user, get_high_score, update_high_score

# Game States
MAIN_MENU = 0
GAME_RUNNING = 1
PAUSED = 2
GAME_OVER = 3

# Power-up variables
POWER_UP_SIZE = 20
POWER_UP_DURATION = 5000  # Duration in milliseconds (5 seconds)
special_brick_types = ["increase_paddle_size", "slow_ball", "extra_life"]  # Power-up types

class BreakoutGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()

        # Game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.row_range = 5
        self.bricks = self.create_bricks(self.row_range, 10)
        self.particles = []  # Particle effects
        self.fragments = []  # Brick fragments
        self.stars = [Star() for _ in range(100)]  # Background stars
        self.level = 1
        self.score = 0
        self.current_high_score = 0
        self.lives = 3
        self.stage_bricks = len(self.bricks)
        self.active_power_up = None
        self.power_ups = []
        self.power_up_start_time = 0
        self.paddle_width_default = self.paddle.rect.width

        # Load sounds needed
        self.game_over_sound = pygame.mixer.Sound("../sounds/lose_sound.wav") # Load game over sound
        pygame.mixer.music.load("../sounds/background_music.mp3")  # Load background music
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

        self.game_state = MAIN_MENU
        self.logged_in = False
        self.current_user = None
        self.focused = True  # To track if the window is in focus

        self.font = pygame.font.Font(None, 36)  # Font for text

        # Load user data
        load_users_from_file()

        pygame.mixer.music.play(-1)  # Start playing background music (loop it indefinitely)

    def create_bricks(self, rows, cols):
        bricks = []
        for row in range(rows):
            for col in range(cols):
                brick = Brick(col * 80 + 10, row * 30 + 10)
                if random.random() < 0.2:  # 20% chance of being a special brick
                    power_up_type = random.choice(special_brick_types)
                    brick.power_up_type = power_up_type
                bricks.append(brick)
        return bricks

    def activate_power_up(self, power_up_type):
        if power_up_type == "increase_paddle_size":
            self.paddle.rect.width = self.paddle_width_default * 1.5  # Increase paddle size
        elif power_up_type == "slow_ball":
            self.ball.dx *= 0.7  # Slow down the ball speed
            self.ball.dy *= 0.7
        elif power_up_type == "extra_life":
            self.lives += 1  # Add extra life

        self.active_power_up = power_up_type
        self.power_up_start_time = pygame.time.get_ticks()

    def reset_power_ups(self):
        if self.active_power_up == "increase_paddle_size":
            self.paddle.rect.width = self.paddle_width_default  # Reset paddle size
        elif self.active_power_up == "slow_ball":
            self.ball.dx /= 0.7  # Restore ball speed
            self.ball.dy /= 0.7

        self.active_power_up = None

    def run(self):
        while True:
            self.handle_events()  # Handle events such as quit, focus loss, etc.
            if self.focused and self.game_state != GAME_OVER:
                self.update_game()  # Only update the game if in focus and not game over
            self.draw_game()  # Draw the game regardless of focus to keep screen updated
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Handle window focus loss and regain
            if event.type == pygame.WINDOWFOCUSLOST:
                self.focused = False  # Pause the game when focus is lost
            if event.type == pygame.WINDOWFOCUSGAINED:
                self.focused = True  # Resume game when focus is regained

            # Handle key presses (only if event is a key event)
            if event.type == pygame.KEYDOWN:
                # Handle key presses in the main menu
                if self.game_state == MAIN_MENU:
                    if event.key == pygame.K_RETURN and self.logged_in:
                        self.game_state = GAME_RUNNING
                        pygame.mixer.music.play(-1)  # Start or resume background music
                    elif event.key == pygame.K_r:
                        self.register_user()
                    elif event.key == pygame.K_l:
                        self.login_user()

                # Handle key presses when the game is running
                if self.game_state == GAME_RUNNING:
                    if event.key == pygame.K_p:
                        self.game_state = PAUSED
                        pygame.mixer.music.pause()  # Pause background music

                # Handle key presses in the pause screen
                if self.game_state == PAUSED:
                    if event.key == pygame.K_RETURN:
                        self.game_state = GAME_RUNNING
                        pygame.mixer.music.unpause()  # Resume background music

                # Handle key presses in the game over screen
                if self.game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()

    def check_collision_with_bricks(self, bricks, particles, fragments):
        self.brick_break_sound = pygame.mixer.Sound("../sounds/destroy_sound.wav") # Load brick break sound
        self.paddle_hit_sound = pygame.mixer.Sound("../sounds/hit_paddle.wav")  # Load paddle hit sound
        for brick in bricks[:]:
            if self.ball.rect.colliderect(brick.rect):
                self.ball.dy = -self.ball.dy  # Bounce off the brick
                pygame.mixer.Sound.play(self.paddle_hit_sound) # Play brick break sound

                if brick.power_up_type:  # If the brick has a power-up
                    power_up = PowerUp(brick.rect.x + 25, brick.rect.y, brick.power_up_type)
                    self.power_ups.append(power_up)
                    print(f"Power-up created: {brick.power_up_type}")
                bricks.remove(brick)

                # Create fire particles when a brick is destroyed
                for _ in range(10):
                    particles.append(Particle(brick.rect.centerx, brick.rect.centery))

                # Break the brick into fragments
                num_fragments = random.randint(4, 10)  # Random number of fragments
                for _ in range(num_fragments):
                    fragments.append(brick.break_into_fragments())

    def update_game(self):
        if self.game_state == GAME_RUNNING:
            self.ball.move()
            self.ball.check_collision_with_walls()
            
            # Paddle movement with arrow keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move(-9)
            if keys[pygame.K_RIGHT]:
                self.paddle.move(9)

            # Update star background
            for star in self.stars:
                star.update()

            self.ball.check_collision_with_paddle(self.paddle, self.particles)
            self.check_collision_with_bricks(self.bricks, self.particles, self.fragments)

            # Update particles and fragments
            for particle in self.particles[:]:
                particle.update()
                if particle.lifetime <= 0 or particle.size <= 0:
                    self.particles.remove(particle)

            for fragment in self.fragments[:]:
                fragment.update()
                if fragment.width <= 0 or fragment.height <= 0:
                    self.fragments.remove(fragment)

            # Check to update score (when brick destroyed)
            if  len(self.bricks) < self.stage_bricks:
                self.scoring()
                
            # Check for level up (all bricks are cleared)
            if len(self.bricks) == 0:
                self.level_up()

            # Check for game over (if ball hits bottom) 
            if self.ball.rect.bottom >= 600 and self.lives > 1: 
                self.lives -= 1 # Deducts a life
                self.paddle = Paddle()
                self.ball = Ball()
            if self.ball.rect.bottom >= 600 and self.lives == 1:    
                self.update_high_score()
                self.current_high_score = get_high_score(self.current_user) # Get the current high score for the logged-in user
                pygame.mixer.Sound.play(self.game_over_sound) # Play game over sound
                self.game_state = GAME_OVER  # Change to GAME_OVER state when player loses

            # Power-up movement and collection
            for power_up in self.power_ups[:]:
                power_up.move()  # Power-ups fall downwards

                if power_up.rect.colliderect(self.paddle.rect):
                    self.activate_power_up(power_up.power_up_type)
                    self.power_ups.remove(power_up)

                if power_up.rect.top >= 600:
                    self.power_ups.remove(power_up)

            if self.active_power_up and pygame.time.get_ticks() - self.power_up_start_time > POWER_UP_DURATION:
                self.reset_power_ups()

    def scoring(self):
        bricks_destroyed = self.stage_bricks - len(self.bricks)  # Only count bricks from the current level
        self.score += bricks_destroyed * (self.level * 100)  # Add points incrementally
        self.stage_bricks = len(self.bricks)  # Update stage_bricks to reflect the remaining bricks

    def level_up(self):
        speed_increase = 1.1
        self.level += 1
        self.row_range += 1
        # Set the next level
        self.paddle = Paddle()
        self.ball = Ball()
        self.ball.dx *= speed_increase
        self.ball.dy *= speed_increase
        self.particles = []
        self.fragments = []
        if self.row_range > 10:
            self.row_range = 10
        self.bricks = self.create_bricks(self.row_range, 10)
        self.stage_bricks = len(self.bricks)
        self.game_state = GAME_RUNNING

    def draw_game(self):
        self.screen.fill((0, 0, 0))  # Black background

        if self.game_state == MAIN_MENU:
            self.draw_main_menu()
        elif self.game_state == GAME_RUNNING:
            self.draw_game_running()
        elif self.game_state == PAUSED:
            self.draw_paused_screen()
        elif self.game_state == GAME_OVER:
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_main_menu(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        menu_text = "Press Enter to Start the Game" if self.logged_in else "Please Login (L) or Register (R)"
        menu_label = self.font.render(menu_text, True, (255, 255, 255))
        # Position the main label at the center of the screen (400 is assumed to be half the width of the screen)
        menu_label_x = 400 - menu_label.get_width() // 2
        menu_label_y = 300
        # Blit the main menu text to the screen
        self.screen.blit(menu_label, (menu_label_x, menu_label_y))
        high_score_text = f"High Score: {self.current_high_score}" if self.logged_in else ""
        high_score_label = self.font.render(high_score_text, True, (255, 255, 255))
        high_score_x = 400 - high_score_label.get_width() // 2
        high_score_y = menu_label_y + menu_label.get_height() + 20
        self.screen.blit(high_score_label, (high_score_x, high_score_y))

        # Blit the high score text to the screen
        self.screen.blit(high_score_label, (high_score_x, high_score_y))

    def draw_game_running(self):
        # Draw the level text
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_text, (400 - level_text.get_width() // 2, 295))

        # Draw the score text
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 320))   

        # Draw the lives text
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (400 - lives_text.get_width() // 2, 345))   

        # Draw stars, paddle, ball, bricks, particles, and fragments
        for star in self.stars:
            star.draw(self.screen)

        # Draw active power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen, power_up.power_up_type)

        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        for particle in self.particles:
            particle.draw(self.screen)
        for fragment in self.fragments:
            fragment.draw(self.screen)

    def draw_paused_screen(self):
        self.screen.fill((0, 0, 0))  # Black background
        label = self.font.render("Paused - Press Enter to Resume", True, (255, 255, 255))
        self.screen.blit(label, (400 - label.get_width() // 2, 300))

    def draw_game_over_screen(self):
        self.screen.fill((0, 0, 0))  # Black background
        label = self.font.render("Game Over - Press R to Restart", True, (255, 255, 255))
        self.screen.blit(label, (400 - label.get_width() // 2, 300))

    def register_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        register_user(username, password)
        print(f"User {username} registered!")

    def login_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if login_user(username, password):
            self.logged_in = True
            self.current_user = username
            self.current_high_score = get_high_score(self.current_user)
            print(f"Welcome back, {username}! Your current high score is {self.current_high_score}.")
        else:
            print("Incorrect username or password")

    def update_high_score(self):
        current_high_score = get_high_score(self.current_user)
        if self.score > current_high_score: # Update the high score if the new score is higher
            update_high_score(self.current_user, self.score)  # Update high score in user_auth
            print(f"New high score for {self.current_user}: {self.score}")
            current_high_score = self.score


    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(col * 80 + 10, row * 30 + 10) for row in range(5) for col in range(10)]
        self.particles = []
        self.fragments = []
        self.score = 0
        self.level = 1
        self.lives = 3
        self.stage_bricks = len(self.bricks)
        self.game_state = MAIN_MENU
        
        

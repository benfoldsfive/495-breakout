"""
Breakout Game Class
--------------
This is a Python implementation of the classic Breakout game using the Pygame library.
The game includes features such as multiple levels, power-ups, particle effects, and background music.
It also has user authentication for tracking high scores and progress, with login and registration functionality.
"""

import random

import pygame
from pathlib import Path
from paddle import Paddle
from ball import Ball
from brick import Brick
from particle import Particle
from power_up import PowerUp
from star import Star
from user_auth import load_users_from_file, register_user, login_user, get_high_score, update_high_score
from text_input_box import TextInputBox
from passtext_input_box import PassTextInputBox
from button import Button

# Game States
MAIN_MENU = 0 # Initial menu where the user can log in or register
GAME_RUNNING = 1 # The game loop where gameplay occurs
PAUSED = 2 # Pauses the game
GAME_OVER = 3 # Displays when the player loses all lives
POST_LOGIN_MENU = 4 # Menu shown after a successful login, before starting the game

# Power-up variables
POWER_UP_SIZE = 20
POWER_UP_DURATION = 5000  # Duration in milliseconds (5 seconds)
special_brick_types = ["increase_paddle_size", "slow_ball", "extra_life"]  # Power-up types


current_dir = Path(__file__).parent.resolve() # Get the current directory
sounds_dir = current_dir.parent / "sounds" # Navigate to the sounds directory 

class BreakoutGame:
    """
    BreakoutGame Class:
    Handles all aspects of the game, including initializing the game, running game states,
    managing player input, collisions, power-ups, scoring, and rendering graphics.
    """

    def __init__(self):
        # Initialize Pygame modules
        pygame.init()
        pygame.mixer.init()

        # Set up the display and clock
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()

        # Initialize game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.default_ball_dx = self.ball.dx
        self.default_ball_dy = self.ball.dx
        self.row_range = 5 # Number of rows of bricks in the current level
        self.bricks = self.create_bricks(self.row_range, 10) # Create the brick layout

        self.particles = []  # Particle effects
        self.fragments = []  # Brick fragments
        self.stars = [Star() for _ in range(100)]  # Background stars for visual effects

        # Game variables
        self.level = 1
        self.score = 0
        self.current_high_score = 0
        self.lives = 3
        self.stage_bricks = len(self.bricks) # Tracks the number of bricks in the current stage
        self.active_power_up = None # Tracks the active power-up
        self.power_ups = [] # List of power-ups
        self.power_up_start_time = 0
        self.paddle_width_default = self.paddle.rect.width

        # Load background music
        pygame.mixer.music.load(sounds_dir / "background_music.mp3")  # Load background music
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

        # Game state variables
        self.game_state = MAIN_MENU
        self.logged_in = False # Tracks if a user is logged in
        self.current_user = None # Stores the current logged-in user
        self.focused = True  # Track if the window is in focus

        # User input for authentication
        self.username_input = TextInputBox(300, 250, 200, 50)
        self.password_input = PassTextInputBox(300, 350, 200, 50)

        # Buttons for login and registration
        self.login_button = Button(300, 450, 200, 50, "Login")
        self.register_button = Button(300, 520, 200, 50, "Register")

        # Font for rendering text
        self.font = pygame.font.Font(None, 36)  # Font for text

        # Load user data
        load_users_from_file()

        pygame.mixer.music.play(-1)  # Start playing background music (loop it indefinitely)

    def create_bricks(self, rows, cols):
        """
        Creates a grid of bricks with optional power-ups assigned to some bricks.
        Arguments:
            - rows: The number of rows of bricks
            - cols: The number of columns of bricks
        Returns:
            - bricks: A list of Brick objects
        """
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
        """
        Activates the specified power-up for the player.
        Arguments:
            - power_up_type: The type of power-up to activate
        """
        activate_power_up = pygame.mixer.Sound(sounds_dir / "power_up_activate.wav")  # Load activation sound for power up
        pygame.mixer.Sound.play(activate_power_up) # Play activation sound for power up

        # Activate power-up based on its type
        if power_up_type == "increase_paddle_size":
            self.paddle.rect.width = self.paddle_width_default * 1.5  # Increase paddle size
        elif power_up_type == "slow_ball":
            slow_ball_dx = self.ball.dx * 0.7
            slow_ball_dy = self.ball.dy * 0.7
            self.ball.dx = slow_ball_dx # Slow down the ball speed
            self.ball.dy = slow_ball_dy
        elif power_up_type == "extra_life":
            self.lives += 1  # Add extra life

        # Track the activated power-up and its start time
        self.active_power_up = power_up_type
        self.power_up_start_time = pygame.time.get_ticks()

    def reset_power_ups(self):
        """
        Resets any active power-up effects back to the default state.
        """
        if self.active_power_up == "increase_paddle_size":
            self.paddle.rect.width = self.paddle_width_default  # Reset paddle size
        elif self.active_power_up == "slow_ball":
            # Preserve current direction of the ball
            direction_x = 1 if self.ball.dx > 0 else -1
            direction_y = 1 if self.ball.dy > 0 else -1

            # Reset speed and apply preserved direction
            self.ball.dx = self.default_ball_dx * direction_x
            self.ball.dy = self.default_ball_dy * direction_y

        self.active_power_up = None # Clear the active power-up

    def run(self):
        """
        Activates main game loop.
        """
        while True:
            self.handle_events()  # Handle events such as quit, focus loss, etc.
            if self.focused: # Update game if the window is focused
                if self.game_state == GAME_RUNNING: # If the game is in the running state
                    self.update_game() # Update game elements like ball, paddle, etc.
                elif self.game_state == POST_LOGIN_MENU:
                    self.draw_post_login_menu()  # Only update the game if in focus and not game over
            self.draw_game()  # Draw the game regardless of focus to keep screen updated
            self.clock.tick(60) # Limit the frame rate to 60 FPS

    def handle_events(self):
        """
        Handles the various events of the main game loop.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user closes the window
                pygame.quit()
                exit()

            # Handle window focus loss and regain
            if event.type == pygame.WINDOWFOCUSLOST:
                self.focused = False  # Pause the game when focus is lost
            if event.type == pygame.WINDOWFOCUSGAINED:
                self.focused = True  # Resume game when focus is regained

            # Handle events in the main menu
            if self.game_state == MAIN_MENU:
                self.username_input.handle_event(event) # Handle username input
                self.password_input.handle_event(event)  # Handle password input

                if self.login_button.handle_event(event): # If the login button is pressed
                    self.login_user() # Handle user login
                elif self.register_button.handle_event(event): # If the register button is pressed
                    self.register_user() # Handle user registration

            # Handle eveents in the post login menu
            if self.game_state == POST_LOGIN_MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = GAME_RUNNING # Start the game when Enter is pressed
                        pygame.mixer.music.play(-1) # Play background music in a loop

            # Handle key presses when the game is running
            if self.game_state == GAME_RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game_state = PAUSED # Pause the game if 'P' is pressed
                        pygame.mixer.music.pause()  # Pause background music

            # Handle key presses in the pause screen
            if self.game_state == PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_state = GAME_RUNNING # Resume the game when Enter is pressed
                    pygame.mixer.music.unpause()  # Resume background music

            # Handle key presses in the game over screen
            if self.game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()

    def check_collision_with_bricks(self, bricks, particles, fragments):
        """
        Check for collisions between the ball and the bricks, handle brick destruction,
        power-up creation, particle effects, and breaking bricks into fragments.

        Parameters:
            - bricks (list): A list of brick objects currently in the game.
            - particles (list): A list that will store particle effects (e.g., fire particles)
                        created when a brick is destroyed.
            - fragments (list): A list that will store the brick fragments generated upon breaking.
                        These fragments are used for visual effects when a brick is destroyed.
        """

        # Load sound effects for brick breaking and power-up drop
        brick_break_sound = pygame.mixer.Sound(sounds_dir / "destroy_sound.wav") # Load brick break sound
        power_up_drop_sound = pygame.mixer.Sound(sounds_dir / "power_up_drop.wav")  # Load power-up drop sound

        # Check collision between ball and bricks
        for brick in bricks[:]:  # Iterate through a copy of the bricks list
            if self.ball.rect.colliderect(brick.rect):  # If ball collides with a brick
                self.ball.dy = -self.ball.dy  # Bounce off the brick
                pygame.mixer.Sound.play(brick_break_sound) # Play brick break sound

                if brick.power_up_type:  # If the brick has a power-up
                    power_up = PowerUp(brick.rect.x + 25, brick.rect.y, brick.power_up_type)
                    self.power_ups.append(power_up) # Add power-up to the list
                    pygame.mixer.Sound.play(power_up_drop_sound) # Play power-up drop sound

                bricks.remove(brick)    # Remove the brick from the list

                # Create fire particles when a brick is destroyed
                for _ in range(10):
                    particles.append(Particle(brick.rect.centerx, brick.rect.centery))

                # Break the brick into fragments
                num_fragments = random.randint(4, 10)  # Random number of fragments
                for _ in range(num_fragments):
                    fragments.append(brick.break_into_fragments())

    def update_game(self):
        """
        Update the game state, handle user input for paddle movement,
        check for collisions, update particles and fragments, manage power-ups,
        and determine game over or level up conditions.
        """
        game_over = pygame.mixer.Sound(sounds_dir / "game_over.wav") # Load sound for game over sound
        lose_life = pygame.mixer.Sound(sounds_dir / "lost_life.wav") # Load sound for a lost life
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
                pygame.mixer.Sound.play(lose_life) # Play sound for a lost life
                self.ball = Ball()
            if self.ball.rect.bottom >= 600 and self.lives == 1:    
                self.update_high_score()
                self.current_high_score = get_high_score(self.current_user) # Get the current high score for the logged-in user
                pygame.mixer.Sound.play(game_over) # Play game over sound
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
        """
        Update the player's score based on the number of bricks destroyed
        in the current level. The score is incremented based on the level
        and the number of bricks that were present.
        """
        bricks_destroyed = self.stage_bricks - len(self.bricks)  # Only count bricks from the current level
        self.score += bricks_destroyed * (self.level * 100)  # Add points incrementally
        self.stage_bricks = len(self.bricks)  # Update stage_bricks to reflect the remaining bricks

    def level_up(self):
        """
        Handle the transition to the next level by increasing the level number,
        adjusting paddle and ball speed, and creating a new set of bricks.
        The game state is set back to GAME_RUNNING.
        """
        speed_increase = 1.1
        self.level += 1
        self.row_range += 1

        # Set the next level
        self.paddle = Paddle()
        self.ball = Ball()
        self.ball.dx *= speed_increase
        self.ball.dy *= speed_increase
        self.default_ball_dx = self.ball.dx
        self.default_ball_dy = self.ball.dy
        self.particles = []
        self.fragments = []

        if self.row_range > 10:
            self.row_range = 10

        self.bricks = self.create_bricks(self.row_range, 10)
        self.stage_bricks = len(self.bricks)
        self.game_state = GAME_RUNNING

    def draw_game(self):
        """
        Render the current game state on the screen, including the main menu,
        game running visuals, post-login menu, paused screen, or game over screen.
        """
        self.screen.fill((0, 0, 0))  # Black background

        if self.game_state == MAIN_MENU:
            self.draw_main_menu()
        elif self.game_state == GAME_RUNNING:
            self.draw_game_running()
        elif self.game_state == POST_LOGIN_MENU:
            self.draw_post_login_menu()
        elif self.game_state == PAUSED:
            self.draw_paused_screen()
        elif self.game_state == GAME_OVER:
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_main_menu(self):
        """
        Draw the main menu interface, including the title, input fields for
        username and password, and buttons for login and registration.
        """
        self.screen.fill((0, 0, 0))  # Set background color to black

        # Draw the main menu title
        title_font = pygame.font.Font(None, 64)  # Larger font for the title
        menu_label = title_font.render("Welcome to Breakout", True, (255, 255, 255))
        self.screen.blit(menu_label, (400 - menu_label.get_width() // 2, 100))

        # Render labels for username and password input fields
        label_font = pygame.font.Font(None, 36)  # Smaller font for labels
        username_label = label_font.render("Username:", True, (255, 255, 255))
        self.screen.blit(username_label, (250, 240))

        password_label = label_font.render("Password:", True, (255, 255, 255))
        self.screen.blit(password_label, (250, 340))

        # Adjust the position of the input boxes
        self.username_input.rect.topleft = (400, 230)
        self.password_input.rect.topleft = (400, 330)

        # Draw input boxes
        self.username_input.draw(self.screen)
        self.password_input.draw(self.screen)

        # Draw the login and register buttons below the input fields with padding
        self.login_button.rect.topleft = (300, 450)  # Adjust position for login button
        self.register_button.rect.topleft = (500, 450)  # Adjust position for register button

        self.login_button.draw(self.screen)
        self.register_button.draw(self.screen)

        # Add an instructional message at the bottom
        instruction_font = pygame.font.Font(None, 28)
        instruction_text = instruction_font.render("Please log in or register to start playing!", True, (200, 200, 200))
        self.screen.blit(instruction_text, (400 - instruction_text.get_width() // 2, 530))

        pygame.display.flip()  # Update the display

    def draw_post_login_menu(self):
        """
        Draw the post-login menu interface that welcomes the user, displays
        the high score, and prompts them to start the game.
        """
        self.screen.fill((0, 0, 0))  # Black background

        # Title: Welcome message
        title_font = pygame.font.Font(None, 64)
        welcome_label = title_font.render(f"Welcome, {self.current_user}!", True, (255, 255, 255))
        self.screen.blit(welcome_label, (400 - welcome_label.get_width() // 2, 200))

        # High Score Display
        score_font = pygame.font.Font(None, 36)
        high_score_label = score_font.render(f"High Score: {self.current_high_score}", True, (255, 255, 255))
        self.screen.blit(high_score_label, (400 - high_score_label.get_width() // 2, 270))

        # Prompt to press Enter
        instruction_font = pygame.font.Font(None, 36)
        instruction_label = instruction_font.render("Press Enter to start the game", True, (200, 200, 200))
        self.screen.blit(instruction_label, (400 - instruction_label.get_width() // 2, 350))

        pygame.display.flip()  # Update the display

    def draw_game_running(self):
        """
        Draw the game's current status during gameplay, including level,
        score, lives, and rendering all game objects such as stars,
        power-ups, paddle, ball, bricks, particles, and fragments.
         """
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
        """
        Draw the paused screen, providing the option to resume.
        """
        self.screen.fill((0, 0, 0))  # Black background
        label = self.font.render("Paused - Press Enter to Resume", True, (255, 255, 255))
        self.screen.blit(label, (400 - label.get_width() // 2, 300))

    def draw_game_over_screen(self):
        """
        Draw the game over screen, displaying the option to restart.
        """
        self.screen.fill((0, 0, 0))  # Black background
        label = self.font.render("Game Over - Press R to Restart", True, (255, 255, 255))
        self.screen.blit(label, (400 - label.get_width() // 2, 300))

    def register_user(self):
        """
        Registers a new user by collecting the username and password from input fields.
        If both fields are filled, it calls the register_user function to store the user's credentials,
        resets the input fields for future entries, and handles any errors related to empty inputs.
        """
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username and password:
            register_user(username, password)   # Clears Text Boxes after registration
            self.username_input.reset()
            self.password_input.reset()
        else:
            print("Username and password cannot be empty.")

    def login_user(self):
        """
        Logs in an existing user by verifying the provided username and password.
        If both fields are filled and the credentials are correct, it updates the logged_in status,
        retrieves the user's high score, and changes the game state to the post-login menu.
        If the credentials are incorrect or empty, it resets the input fields and prints an error message.
        """
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username and password:
            if login_user(username, password):
                self.logged_in = True       # When user data successfully authorized, logged_in set True, Gets User and highscore
                self.current_user = username
                self.current_high_score = get_high_score(self.current_user)
                print(f"Welcome back, {username}! Your high score is {self.current_high_score}.")   # Prints in command line
                self.game_state = POST_LOGIN_MENU   # Sets game state to post login menu
            else:
                self.username_input.reset()     # Username and password fields are cleared when incorrect info inputted
                self.password_input.reset()
                print("Incorrect username or password.")
        else:
            print("Username and password cannot be empty.")

    def update_high_score(self):
        """
        Checks if the current score exceeds the user's high score.
        If it does, updates the high score for the current user in the user_auth database
        and prints a confirmation message.
        """
        current_high_score = get_high_score(self.current_user)
        if self.score > current_high_score: # Update the high score if the new score is higher
            update_high_score(self.current_user, self.score)  # Update high score in user_auth
            print(f"New high score for {self.current_user}: {self.score}")

    def reset_game(self):
        """
        Resets the game state to its initial conditions. This includes reinitializing
        game objects such as the paddle, ball, and bricks, clearing particles and fragments,
        resetting the score, level, lives, and the number of bricks on the stage.
        Also sets the game state to MAIN_MENU.
        """
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(col * 80 + 10, row * 30 + 10) for row in range(5) for col in range(10)]
        self.particles = []
        self.fragments = []
        self.score = 0
        self.level = 1
        self.lives = 3
        self.stage_bricks = len(self.bricks)
        self.game_state = POST_LOGIN_MENU

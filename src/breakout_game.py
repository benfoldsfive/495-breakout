import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from particle import Particle
from star import Star
from user_auth import load_users_from_file, register_user, login_user

# Game States
MAIN_MENU = 0
GAME_RUNNING = 1
PAUSED = 2
GAME_OVER = 3

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
        self.bricks = [Brick(col * 80 + 10, row * 30 + 10) for row in range(5) for col in range(10)]
        self.particles = []  # Particle effects
        self.fragments = []  # Brick fragments
        self.stars = [Star() for _ in range(100)]  # Background stars

        # Load sounds needed
        self.game_over_sound = pygame.mixer.Sound("sounds/lose_sound.wav") # Load game over sound
        pygame.mixer.music.load("sounds/background_music.mp3")  # Load background mussic
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)

        self.game_state = MAIN_MENU
        self.logged_in = False
        self.current_user = None
        self.focused = True  # To track if the window is in focus

        self.font = pygame.font.Font(None, 36)  # Font for text

        # Load user data
        load_users_from_file()

        pygame.mixer.music.play(-1)  # Start playing background music (loop it indefinitely)

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
                        pygame.mixer.music.pause(-1)  # Pause background music

                # Handle key presses in the pause screen
                if self.game_state == PAUSED:
                    if event.key == pygame.K_RETURN:
                        self.game_state = GAME_RUNNING
                        pygame.mixer.music.unpause(-1)  # Resume background music

                # Handle key presses in the game over screen
                if self.game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()

    def update_game(self):
        if self.game_state == GAME_RUNNING:
            self.ball.move()
            self.ball.check_collision_with_walls()

            # Paddle movement with arrow keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move(-5)
            if keys[pygame.K_RIGHT]:
                self.paddle.move(5)

            # Update star background
            for star in self.stars:
                star.update()

            self.ball.check_collision_with_paddle(self.paddle, self.particles)
            self.ball.check_collision_with_bricks(self.bricks, self.particles, self.fragments)

            # Update particles and fragments
            for particle in self.particles[:]:
                particle.update()
                if particle.lifetime <= 0 or particle.size <= 0:
                    self.particles.remove(particle)

            for fragment in self.fragments[:]:
                fragment.update()
                if fragment.width <= 0 or fragment.height <= 0:
                    self.fragments.remove(fragment)

            # Check for game over (if ball hits bottom)
            if self.ball.rect.bottom >= 600:
                pygame.mixer.Sound.play(self.game_over_sound) # Play game over sound
                self.game_state = GAME_OVER  # Change to GAME_OVER state when player loses

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
        text = "Press Enter to Start the Game" if self.logged_in else "Please Login (L) or Register (R)"
        label = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (400 - label.get_width() // 2, 300))

    def draw_game_running(self):
        # Draw stars, paddle, ball, bricks, particles, and fragments
        for star in self.stars:
            star.draw(self.screen)

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
            print(f"Welcome back, {username}!")
        else:
            print("Incorrect username or password")

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(col * 80 + 10, row * 30 + 10) for row in range(5) for col in range(10)]
        self.particles = []
        self.fragments = []
        self.game_state = MAIN_MENU

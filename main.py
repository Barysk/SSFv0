import pygame
import threading

# Initialize Pygame
pygame.init()

# Create a resizable game window
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('SSF_v0')

# Define colors and settings
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
player_speed = 10
projectile_speed = 10
enemy_speed = 5
background_speed = 1
game_running = True
score = 0

# Load the images
player_image_original = pygame.image.load('Sprites/player.png').convert_alpha()
player_image_size = (32, 32)
player_image = pygame.transform.scale(player_image_original, player_image_size)

projectile_image_original = pygame.image.load('Sprites/projectile.png').convert_alpha()
projectile_image_size = (8, 32)
projectile_image = pygame.transform.scale(projectile_image_original, projectile_image_size)

enemy_image_original = pygame.image.load('Sprites/enemy.png').convert_alpha()
enemy_image_size = (32, 32)
enemy_image = pygame.transform.scale(enemy_image_original, enemy_image_size)

background_image = pygame.image.load('Sprites/star_background.png').convert()

# Scale the background to fit the window size and create a duplicate for the infinite scroll effect
background = pygame.transform.scale(background_image, (1280, 720))
background_rect = background.get_rect()
background_copy = background.copy()
background_copy_rect = background_copy.get_rect()
background_copy_rect.y = -background_copy_rect.height

# FPS limit
clock = pygame.time.Clock()

# Load font
font_path = 'Fonts/3270-Regular.ttf'
# font_path = 'PixelifySans-Bold.ttf' # Initial font
font_size = 32
score_font = pygame.font.Font(font_path, font_size)

# Lock for synchronization (used sparingly)
lock = threading.Lock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = player_speed

    def move(self, direction):
        # Update the x-coordinate
        self.rect.x += direction * self.speed
        # Ensure the player doesn't go out of the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = projectile_speed
        self.direction = -1  # Projectiles move upwards

    def update(self):
        self.rect.y += self.direction * self.speed
        if self.rect.bottom <= 0:
            self.kill()  # Remove the projectile when it goes off-screen

def shoot_projectile(player):
    projectile = Projectile(projectile_image, player.rect.midtop)
    all_sprites.add(projectile)
    projectiles.add(projectile)

def move_projectiles():
    """Thread function to manage projectile movements independently."""
    while game_running:
        with lock:
            projectiles.update()
        pygame.time.delay(10)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = enemy_speed
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.direction *= -1
            self.rect.y += self.rect.height

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Add player and enemies to sprite groups
player_sprite = Player(player_image, [640, 650])
all_sprites.add(player_sprite)

enemies = [Enemy(enemy_image, pos) for pos in [[100, 50], [200, 50], [300, 50], [400, 50], [500, 50], [600, 50], [700, 50], [800, 50], [900, 50], [1000, 50], [1100, 50], [1200, 50], [1300, 50], [1400, 50], [1500, 50], [1600, 50], [1700, 50], [1800, 50]]]
for enemy in enemies:
    enemies_group.add(enemy)
    all_sprites.add(enemy)

def move_enemies():
    """Thread function to manage enemy movements independently."""
    while game_running:
        with lock:
            for enemy in enemies:
                enemy.update()
        pygame.time.delay(100)

def draw_score():
    """Function to draw the current score on the screen."""
    score_surface = score_font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(topleft=(10, 10))
    screen.blit(score_surface, score_rect)

def game_loop():
    global game_running, screen, score, enemy_speed

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    shoot_projectile(player_sprite)

        # Handle key inputs
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_sprite.move(-1)
        if keys[pygame.K_RIGHT]:
            player_sprite.move(1)

        # Update background position
        background_rect.y += background_speed
        background_copy_rect.y += background_speed
        if background_rect.top >= screen.get_height():
            background_rect.y = -background_rect.height
        if background_copy_rect.top >= screen.get_height():
            background_copy_rect.y = -background_copy_rect.height

        # Collision detection between player and enemies
        if pygame.sprite.spritecollideany(player_sprite, enemies_group):
            end_game(score)

        # Collision detection between projectiles and enemies
        hits = pygame.sprite.groupcollide(projectiles, enemies_group, True, True)
        for hit in hits:
            score += 1
            if score % 3 == 0:  # Check if score is divisible by 10
                enemy_speed += 1  # Increase enemy speed
                # Update speed for all enemies on the field
                for enemy in enemies_group:
                    enemy.speed = enemy_speed
            if score % 10 == 0:  # Check if score is divisible by 13
                add_new_wave()

        # Move enemies
        enemies_group.update()

        # Rendering
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(background_copy, background_copy_rect)
        draw_score()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def end_game(final_score):
    global game_running, score, enemies_group, enemy_speed, all_sprites

    game_running = False
    screen.fill(BLACK)
    end_font = pygame.font.Font(None, 36)
    end_text = end_font.render(f"Game Over! Final Score: {final_score}", True, WHITE)
    end_rect = end_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 20))
    screen.blit(end_text, end_rect)
    pygame.display.flip()

    # Wait for any key press to quit the game
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                pygame.quit()  # Quit the game
                waiting_for_key = False

def add_new_wave():
    global enemies_group
    new_enemies = [Enemy(enemy_image, pos) for pos in [[100, 50], [200, 50], [300, 50], [400, 50], [500, 50], [600, 50], [700, 50], [800, 50], [900, 50], [1000, 50], [1100, 50], [1200, 50], [1300, 50], [1400, 50], [1500, 50], [1600, 50], [1700, 50], [1800, 50]]]
    for enemy in new_enemies:
        enemy.speed = enemy_speed  # Set speed for new enemies
        enemies_group.add(enemy)
        all_sprites.add(enemy)

# Start enemy movement in a separate thread
enemy_thread = threading.Thread(target=move_enemies)
enemy_thread.start()

# Start projectile movement in a separate thread
projectile_thread = threading.Thread(target=move_projectiles)
projectile_thread.start()

# Start the main game loop in the main thread
game_loop()

# Wait for threads to finish before quitting
enemy_thread.join()
projectile_thread.join()

pygame.quit()

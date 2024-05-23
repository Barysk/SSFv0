import pygame

# Initializes all imported Pygame modules
pygame.init()
pygame.mixer.init()

#Importing sounds
shoot_sound = pygame.mixer.Sound('Sounds/shoot_sound.wav')
death_sound = pygame.mixer.Sound('Sounds/death_sound.wav')
game_over = pygame.mixer.Sound('Sounds/game_over2.wav')
player2_sound = pygame.mixer.Sound('Sounds/player2.wav')
current_volume = 0.5

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('SSF_v0')

# Colors
BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (200, 200, 200)

# Font settings and loading images
FONT_SIZE = 36
font = pygame.font.Font(None, FONT_SIZE)
font_path = 'Fonts/3270-Regular.ttf'
font_size = 32
score_font = pygame.font.Font(font_path, font_size)

# Movement speeds
player_speed = 10
projectile_speed = 10
background_speed = 1
enemy_speed = 10000

# Shooting restrictions
max_projectiles = 10
reload_time = 10  # reload time in seconds

# Counters and timers for reloading
player_shots_left = max_projectiles
player2_shots_left = max_projectiles
last_reload_time = pygame.time.get_ticks()

# Loading image assets with optional resizing
def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

#Resource initialization
player_image = load_image('Sprites/player.png', (32, 32))
projectile_image = load_image('Sprites/projectile.png', (8, 32))
enemy_image = load_image('Sprites/enemy.png', (32, 32))
background_image = load_image('Sprites/star_background.png').convert()
background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

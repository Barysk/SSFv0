import threading
from game_objects import Player, Player2, Projectile, Enemy
from config import *

# Flag to keep the game loop running
game_running = True
score = 0

# Player variables and threading for projectiles and enemies
player2_active = False
player2_sprite = None
background_rect = background.get_rect()
background_copy = background.copy()
background_copy_rect = background_copy.get_rect()
background_copy_rect.y = -background_copy_rect.height

# FPS limit
clock = pygame.time.Clock()

# Lock for synchronization (used sparingly)
lock = threading.Lock()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Add player and enemies to sprite groups
player_sprite = Player(player_image, [300, 650])
all_sprites.add(player_sprite)

enemies = [Enemy(enemy_image, pos) for pos in [[100, 50], [200, 50], [300, 50], [400, 50], [500, 50], [600, 50], [700, 50], [800, 50], [900, 50], [1000, 50], [1100, 50], [1200, 50], [1300, 50], [1400, 50], [1500, 50], [1600, 50], [1700, 50], [1800, 50]]]
for enemy in enemies:
    enemies_group.add(enemy)
    all_sprites.add(enemy)

def shoot_projectile(player):
    projectile = Projectile(projectile_image, player.rect.midtop)
    all_sprites.add(projectile)
    projectiles.add(projectile)

def move_projectiles():
    """Thread function to manage projectile movements independently."""
    global game_running
    while game_running:
        try:
            with lock:
                projectiles.update()
        except pygame.error:
            print("Pygame surface has been closed.")
            break
        pygame.time.delay(10)

def move_enemies():
    """Thread function to manage enemy movements independently."""
    global game_running
    while game_running:
        with lock:
            try:
                if not game_running:
                    break
                for enemy in enemies:
                    enemy.update()
            except pygame.error:
                print("Pygame surface has been closed.")
                break
        pygame.time.delay(100)

def draw_score():
    """Function to draw the current score on the screen."""
    score_surface = score_font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(topleft=(10, 10))
    screen.blit(score_surface, score_rect)

def game_loop():
    global game_running, screen, score, player2_active, enemy_speed

    while game_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False  # Set game_running too False to exit the loop
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    shoot_projectile(player_sprite)
                if player2_active and event.key == pygame.K_w:
                    shoot_projectile(player2_sprite)
                if event.key == pygame.K_F1 and not player2_active:
                    player2_active = True
                    player2_sprite = Player2(player_image, [900, 650])
                    all_sprites.add(player2_sprite)
                if event.key == pygame.K_ESCAPE:
                    game_running = False  # Stop the game loop on ESC key press

        # Handle key inputs for player 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_sprite.move(-1)
        if keys[pygame.K_RIGHT]:
            player_sprite.move(1)

        # Handle key inputs for player 2 if active
        if player2_active:
            if keys[pygame.K_a]:  # Player 2 moves left
                player2_sprite.move(-1)
            if keys[pygame.K_d]:  # Player 2 moves right
                player2_sprite.move(1)

        # Update background position
        background_rect.y += background_speed
        background_copy_rect.y += background_speed
        if background_rect.top >= screen.get_height():
            background_rect.y = -background_rect.height
        if background_copy_rect.top >= screen.get_height():
            background_copy_rect.y = -background_copy_rect.height

        # Check if the game is still running before updating the enemies group
        if game_running:
            enemies_group.update()

        # Collision detection between player and enemies
        if pygame.sprite.spritecollideany(player_sprite, enemies_group) or (player2_active and pygame.sprite.spritecollideany(player2_sprite, enemies_group)):
            end_game(score)

        # Collision detection between projectiles and enemies
        hits = pygame.sprite.groupcollide(projectiles, enemies_group, True, True)
        for hit in hits:
            score += 1
            if score % 10 == 0:  # Check if score is divisible by 10
                enemy_speed += 1  # Increase enemy speed
                # Update speed for all enemies on the field
                for enemy in enemies_group:
                    enemy.speed = enemy_speed
            if score % 11 == 0:  # Check if score is divisible by givennumber
                add_new_wave()

        # Rendering
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(background_copy, background_copy_rect)
        draw_score()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def end_game(final_score):
    global game_running, score, enemies_group, all_sprites

    game_running = False
    screen.fill(BLACK)
    end_font = pygame.font.Font(None, 64)
    end_text = end_font.render(f"Game Over! Final Score: {final_score}", True, WHITE)
    end_rect = end_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 20))
    screen.blit(end_text, end_rect)
    pygame.display.flip()

    # Wait for any key press to quit the game
    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting_for_key = False

def restart_game():
    global game_running, score, enemies_group, all_sprites, enemy_thread, projectile_thread, player_sprite, player2_sprite, player2_active, enemy_speed

    # Ensure game threads are not running
    game_running = False
    if enemy_thread.is_alive():
        enemy_thread.join()
    if projectile_thread.is_alive():
        projectile_thread.join()

    # Reset game variables
    score = 0
    player2_active = False
    enemy_speed = 5  # Reset enemy speed to its initial value

    # Clear sprite groups
    enemies_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    game_running = True

    # Recreate player and initial set of enemies
    player_sprite = Player(player_image, [300, 650])
    all_sprites.add(player_sprite)
    add_new_wave()  # Add an initial wave of enemies with default speed

    # Restart threads
    enemy_thread = threading.Thread(target=move_enemies)
    projectile_thread = threading.Thread(target=move_projectiles)
    enemy_thread.start()
    projectile_thread.start()


def add_new_wave():
    global enemies_group, enemy_speed
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

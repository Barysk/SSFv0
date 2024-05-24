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

def shoot_projectile(player, is_player2=False):
    global player_shots_left, player2_shots_left

    if is_player2:
        if player2_shots_left > 0:
            projectile = Projectile(projectile_image, player.rect.midtop)
            all_sprites.add(projectile)
            projectiles.add(projectile)
            shoot_sound.play()
            player2_shots_left -= 1
    else:
        if player_shots_left > 0:
            projectile = Projectile(projectile_image, player.rect.midtop)
            all_sprites.add(projectile)
            projectiles.add(projectile)
            shoot_sound.play()
            player_shots_left -= 1

def reload_projectiles():
    global last_reload_time, player_shots_left, player2_shots_left

    current_time = pygame.time.get_ticks()
    if current_time - last_reload_time > reload_time * 1000:  # reload in seconds
        player_shots_left = max_projectiles
        player2_shots_left = max_projectiles
        last_reload_time = current_time


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

def draw_projectiles():
    """Function to draw available projectiles on the screen."""
    proj_surface = score_font.render(f'Shots left: {player_shots_left}', True, WHITE)
    score_rect = proj_surface.get_rect(topleft=(10, 40))
    screen.blit(proj_surface, score_rect)
def draw_slider(screen, x, y, width, height, percentage):
    """Draws a volume slider."""
    pygame.draw.rect(screen, GRAY, (x, y, width, height))  # Slider background
    slider_pos = x + int(percentage * width)  # Calculate slider knob position
    pygame.draw.circle(screen, WHITE, (slider_pos, y + height // 2), height // 2)  # Slider knob
    return pygame.Rect(x, y, width, height), slider_pos

def handle_slider_events(slider_rect, mx, my, button_down):
    """Handles mouse events on the volume slider."""
    static_slider_x = slider_rect.x + int(current_volume * slider_rect.width)  # Current slider position
    if button_down and slider_rect.collidepoint(mx, my):
        # Calculate new volume based on mouse position within the slider bounds
        new_x = max(slider_rect.x, min(mx, slider_rect.right))
        new_volume = (new_x - slider_rect.x) / slider_rect.width
        return new_volume
    return None

lock = threading.Lock()

def resize_background(width, height):
    """ Scales both background images according to the current window size. """
    global background, background_rect, background_copy, background_copy_rect
    with lock:
        background = pygame.transform.scale(background_image, (width, height))
        background_copy = pygame.transform.scale(background_image, (width, height))
        background_rect = background.get_rect()
        background_copy_rect = background.get_rect()
        background_copy_rect.y = -background_copy_rect.height

def game_loop():
    global game_running, screen, score, player2_active, enemy_speed

    while game_running:
        reload_projectiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False  # Set game_running too False to exit the loop
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                resize_background(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    shoot_projectile(player_sprite)
                if player2_active and event.key == pygame.K_w:
                    shoot_projectile(player2_sprite)
                if event.key == pygame.K_F1 and not player2_active:
                    player2_active = True
                    player2_sprite = Player2(player2_image, [900, 650])
                    player2_sound.play()
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
            death_sound.play()
            score += 1
            '''
            if score % 10 == 0:  # Check if score is divisible by 10
                enemy_speed += 1  # Increase enemy speed
                # Update speed for all enemies on the field
                for enemy in enemies_group:
                    enemy.speed = enemy_speed
                '''
            if score % 11 == 0:  # Check if score is divisible by given number
                add_new_wave()

        # Rendering
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(background_copy, background_copy_rect)
        draw_score()
        draw_projectiles()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def end_game(final_score):
    global game_running, score, enemies_group, all_sprites

    game_running = False
    screen.fill(BLACK)
    end_font = pygame.font.Font(None, 64)
    game_over.play()
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
    #for game over sound demonstration
    #enemy_speed = 100

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

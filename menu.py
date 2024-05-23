import pygame
import sys
from Game import game_loop, restart_game, draw_slider, handle_slider_events
from config import BLACK, WHITE, GRAY, font, game_over, shoot_sound, death_sound, current_volume

# Utility function to draw text with the top left corner at a specific location
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Utility function to draw text centered within a specified rectangle
def draw_text_centered(text, font, color, surface, rect):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=rect.center)
    surface.blit(textobj, textrect)

# Displays the main menu interface, handling interactions and navigation
def main_menu(screen, font):
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, 20, 20)  # Draw the main menu title at the top-left corner

        # Get the current mouse position
        mx, my = pygame.mouse.get_pos()

        # Define buttons as rectangles for interaction
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 160, 200, 50)
        button_3 = pygame.Rect(50, 220, 200, 50)

        # Draw buttons and label them
        pygame.draw.rect(screen, GRAY, button_1)
        draw_text('Start', font, WHITE, screen, 70, 110)
        pygame.draw.rect(screen, GRAY, button_2)
        draw_text('Options', font, WHITE, screen, 70, 170)
        pygame.draw.rect(screen, GRAY, button_3)
        draw_text('Exit', font, WHITE, screen, 70, 230)

        # Variable to check if the mouse was clicked
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Check if a button was clicked and respond accordingly
        if button_1.collidepoint((mx, my)) and click:
            restart_game()  # Restart the game processes
            game_loop()  # Start the game
        if button_2.collidepoint((mx, my)) and click:
            options(screen, font)  # Enter options menu
        if button_3.collidepoint((mx, my)) and click:
            pygame.quit()
            sys.exit()

        # Update the display to show changes
        pygame.display.update()

# Submenu for adjusting screen options like window size
def options(screen, font):
    running = True  # Control the loop execution
    dragging = False  # Indicates if the slider is being dragged
    left_margin = 50  # Margin from the left side for buttons
    button_width = 200
    button_height = 50
    vertical_spacing = 20  # Vertical spacing between buttons

    # Define the positions for screen resolution buttons
    button_hd = pygame.Rect(left_margin, 250, button_width, button_height)
    button_fullhd = pygame.Rect(left_margin, 250 + button_height + vertical_spacing, button_width, button_height)
    volume_slider_rect = pygame.Rect(50, 400, 200, 10)  # Volume slider rectangle

    while running:
        screen.fill(BLACK)  # Clear the screen with black color

        # Draw the 'Options' title and 'Press ESC to return' instruction
        draw_text('Options', font, WHITE, screen, left_margin, 50)
        draw_text('Press ESC to return', font, WHITE, screen, left_margin, 550)

        # Draw resolution change buttons
        pygame.draw.rect(screen, GRAY, button_hd)
        draw_text_centered('Window', font, WHITE, screen, button_hd)
        pygame.draw.rect(screen, GRAY, button_fullhd)
        draw_text_centered('Full Screen', font, WHITE, screen, button_fullhd)

        mx, my = pygame.mouse.get_pos()  # Get the current mouse position

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the Pygame
                sys.exit()  # Exit the program
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Start dragging if mouse is over the slider
                if volume_slider_rect.collidepoint(mx, my):
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False  # Stop dragging on mouse button release

            # Handle the Escape key to exit the options menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit the options function and return to the previous menu

        if dragging:
            # Handle slider movement and adjust volume if dragging
            new_volume = handle_slider_events(volume_slider_rect, mx, my, True)
            if new_volume is not None:
                adjust_volume(new_volume)  # Adjust the global volume based on the slider's position

        # Redraw the volume slider with the updated volume level
        draw_slider(screen, volume_slider_rect.x, volume_slider_rect.y, volume_slider_rect.width, volume_slider_rect.height, current_volume)

        # Update the display to show changes
        pygame.display.update()

def adjust_volume(volume):
    global current_volume
    current_volume = volume
    pygame.mixer.music.set_volume(current_volume)
    for sound in [shoot_sound, death_sound, game_over]:
        sound.set_volume(current_volume)
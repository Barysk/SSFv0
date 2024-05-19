import pygame
import sys
from Game import game_loop

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_text_centered(text, font, color, surface, rect):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=rect.center)
    surface.blit(textobj, textrect)

def main_menu(screen, font):
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 160, 200, 50)
        button_3 = pygame.Rect(50, 220, 200, 50)

        pygame.draw.rect(screen, GRAY, button_1)
        draw_text('Start', font, WHITE, screen, 70, 110)
        pygame.draw.rect(screen, GRAY, button_2)
        draw_text('Options', font, WHITE, screen, 70, 170)
        pygame.draw.rect(screen, GRAY, button_3)
        draw_text('Exit', font, WHITE, screen, 70, 230)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_1.collidepoint((mx, my)) and click:
            game_loop()  # Start the game
        if button_2.collidepoint((mx, my)) and click:
            options(screen, font)  # Enter options menu
        if button_3.collidepoint((mx, my)) and click:
            pygame.quit()
            sys.exit()

        pygame.display.update()

def options(screen, font):
    running = True
    left_margin = 50  # Margin from the left side for buttons
    button_width = 200
    button_height = 50
    vertical_spacing = 20  # Space between buttons

    # Define button positions
    button_hd = pygame.Rect(left_margin, 250, button_width, button_height)
    button_fullhd = pygame.Rect(left_margin, 250 + button_height + vertical_spacing, button_width, button_height)

    while running:
        screen.fill(BLACK)

        # Draw titles and ESC instruction
        draw_text('Options', font, WHITE, screen, left_margin, 50)  # Move to top left corner
        draw_text('Press ESC to return', font, WHITE, screen, left_margin, 550)  # Move to bottom left corner

        mx, my = pygame.mouse.get_pos()

        # Draw buttons and centered text on them
        pygame.draw.rect(screen, BLACK, button_hd)
        pygame.draw.rect(screen, BLACK, button_fullhd)
        draw_text_centered('Window', font, WHITE, screen, button_hd)
        draw_text_centered('Full Screen', font, WHITE, screen, button_fullhd)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_hd.collidepoint((mx, my)):
                    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                elif button_fullhd.collidepoint((mx, my)):
                    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

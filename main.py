import pygame
import Game
import menu

if __name__ == "__main__":
    menu.main_menu(Game.screen, Game.font)  # Pass screen and font as arguments

    # Wait for threads to finish before quitting
    Game.enemy_thread.join()
    Game.projectile_thread.join()

    pygame.quit()
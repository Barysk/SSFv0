import pygame
import Game
import menu

if __name__ == "__main__":
    # Calls the main menu function from menu module with necessary parameters
    menu.main_menu(Game.screen, Game.font)

    # Waits for both enemy and projectile threads to complete before quitting the program
    Game.enemy_thread.join()
    Game.projectile_thread.join()

    # Terminates all Pygame modules cleanly
    pygame.quit()

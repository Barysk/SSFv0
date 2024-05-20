import pygame
from config import screen, player_speed, projectile_speed, enemy_speed

# Player class definition using Pygame's sprite framework.
class Player(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = player_speed

    # Method to move the player left or right within the screen boundaries
    def move(self, direction):
        self.rect.x += direction * self.speed  # Move the rectangle in the direction multiplied by speed
        # Prevent the player from moving out of the screen's left side
        if self.rect.left < 0:
            self.rect.left = 0
        # Prevent the player from moving out of the screen's right side
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

# Second player class, similar to the first but can be used for multiplayer functionality
class Player2(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = player_speed

    # Method to move the player left or right within the screen boundaries, identical to Player class
    def move(self, direction):
        self.rect.x += direction * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()

# Projectile class to handle the behavior of projectiles fired by the player
class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = projectile_speed
        self.direction = -1

    # Method to update the position of the projectile
    def update(self):
        self.rect.y += self.direction * self.speed  # Move the projectile upward
        # Remove the projectile if it moves off the top of the screen
        if self.rect.bottom <= 0:
            self.kill()  # Remove the sprite from all groups

# Enemy class to manage enemy behavior
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.speed = enemy_speed
        self.direction = 1  # Set initial movement direction to right

    # Method to update the enemy's position
    def update(self):
        self.rect.x += self.direction * self.speed  # Move the enemy left or right
        # Change direction if the enemy hits the left or right edge of the screen
        if self.rect.left <= 0 or self.rect.right >= screen.get_width():
            self.direction *= -1  # Reverse direction
            self.rect.y += self.rect.height  # Move the enemy down a row when direction changes

# SSFv0

## Description

SSFv0 is a 2D arcade-style game wrought using Pygame. Players take the helm of a celestial vessel to vanquish waves of adversaries whilst evading laser beams. The game employs multiple threads to govern the movement of projectiles and foes, ensuring a seamless play experience.

## Threads

1.  **Main Thread**

    -   Handles the main game loop, including event handling, player movements, collision detection, and rendering.
2.  **Projectile Movement Thread**

    -   Manages the movement of projectiles independently of the main game loop to ensure smooth projectile motion.
3.  **Enemy Movement Thread**

    -   Manages the movement of enemies independently of the main game loop to ensure smooth enemy motion.

## Critical Sections

1.  **Projectile Movement**

    -   **Type:** MUTEX (using `threading.Lock()`)
    -   **Description:** Ensures that projectile movements do not conflict with other operations by locking shared resources during updates.
2.  **Enemy Movement**

    -   **Type:** MUTEX (using `threading.Lock()`)
    -   **Description:** Ensures that enemy movements do not conflict with other operations by locking shared resources during updates.
3.  **Background Resizing**

    -   **Type:** MUTEX (using `threading.Lock()`)
    -   **Description:** Ensures the background is correctly resized and displayed during window resizing events without causing conflicts.

## Usage

-   **Start the Game:** Select 'Start' from the main menu.
-   **Options:** Adjust screen resolution and volume settings in the 'Options' menu.
-   **Exit:** Quit the game from the main menu or by pressing ESC during gameplay.'
-   **Second Player:** Press F1 during the game to activate second player.

## Controls

-   **Player 1:**

    -   Move left: Arrow Left
    -   Move right: Arrow Right
    -   Shoot: Arrow Up
-   **Player 2 (if activated):**

    -   Move left: 'A'
    -   Move right: 'D'
    -   Shoot: 'W'


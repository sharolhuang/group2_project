# Space Survival War Documentation

## Overview
Space Survival War is an engaging arcade-style game developed with Python and Pygame. Players control a spaceship, navigating through space, dodging asteroids, battling enemy ships, and collecting power-ups.

## Installation

To set up Space Survival War, follow these steps according to your operating system:

### Windows
1. **Python**: Download from [python.org](https://www.python.org/downloads/windows/) and follow the installer instructions. Check "Add Python to PATH".
2. **Pygame**: In Command Prompt, run `pip install pygame`.

### macOS
1. **Python**: Comes pre-installed or download from [python.org](https://www.python.org/downloads/mac-osx/).
2. **Pygame**: In Terminal, run `pip3 install pygame`.

### Linux
1. **Python**: Usually pre-installed or use package manager (e.g., `sudo apt-get install python3` for Ubuntu).
2. **Pygame**: In Terminal, run `pip3 install pygame`.

After setting up Python and Pygame:
- **Download Game**: Clone or download the repository from GitHub.
- **Run Game**: Navigate to the game folder and run `main.py` using Python.

## Gameplay
- **Controls**: Use arrow keys for navigation, spacebar to shoot.
- **Objectives**: Avoid obstacles, destroy enemies, collect power-ups.
- **Scoring**: Earn points by destroying enemies and asteroids.

## Features
- **Spaceship Customization**: Modify spaceship controls and appearance.
- **Dynamic Difficulty**: Game difficulty scales with player score.
- **Power-Ups**: Enhancements like shields, extra lives, and weapon upgrades.
- **Audio**: Engaging background music and sound effects.

## Code Structure
- `main.py`: Contains the main game loop, event handling, and rendering.
- `Player`, `Rock`, `Bullet`, `Enemy`: Classes representing different game elements with methods for their behavior and rendering.
- `load_image()`, `load_sound()`: Utility functions for loading media.

## Detailed Descriptions

### Player Class
The `Player` class manages the spaceship controlled by the player. It handles various aspects like movement, shooting, lives, health, and power-up effects. Key attributes include health points, number of lives, gun status, and invulnerability. The class also contains methods for updating the spaceship's state, shooting bullets, hiding (when hit), and power-up effects (like gun upgrades or invulnerability).

### Enemy Class
The `Enemy` class represents enemy ships in the game. Each enemy has attributes like health points and a flag for movement (stationary or moving). The class includes methods for updating enemy movement, shooting bullets, and handling damage when hit by the player's bullets.

### Rock Class
The `Rock` class is used for creating asteroid objects. These asteroids move randomly across the screen and rotate. Attributes include speed and rotation degree. The class contains methods for updating the position of the asteroid and handling rotation for a realistic appearance.

## Code Examples

### Creating a Player Object
```python
player = Player()
# This initializes a player object with default attributes like health and lives.
```

### Handling Collisions
```python
def collision_single_with_group(single, group, dokill, collision_handler):
    hits = pygame.sprite.spritecollide(single, group, dokill)
    for hit in hits:
        collision_handler(single, hit)

# Example usage: Detecting collision between the player and rocks
collision_single_with_group(player, rocks, True, rock_player_collision)
```

This code snippet shows how to detect collisions between a single sprite and a group of sprites (like detecting when the player collides with rocks). The `collision_single_with_group` function takes a sprite, a group, and a collision handler function to process the collision.

## Troubleshooting/FAQ
1. **Installation Issues**: Ensure Python and Pygame are correctly installed. Verify Python version compatibility.
2. **Game Crashes**: Check for error messages in the console. Ensure all game assets (images, sounds) are correctly placed in their respective directories.
3. **Sound Problems**: Verify the sound files are correctly loaded and the system volume is not muted.

## Development Notes
- **Design Choices**: Chose Pygame for its simplicity and suitability for 2D games.
- **Challenges Faced**: Implementing smooth movement and collision detection.
- **Solutions**: Utilized Pygame's sprite and collision modules, and optimized game loop for better performance.

## Future Enhancements
- **New Levels**: Adding levels with increasing difficulty.
- **Multiplayer Mode**: Implementing a multiplayer feature.
- **Customization**: Allowing players to customize spaceship appearances.
- **Open Areas for Contribution**: Suggestions for new features or enhancements are welcome.

## Contribution Guidelines
1. **How to Contribute**: Fork the repository, make changes, and submit a pull request.
2. **Coding Standards**: Follow PEP 8 guidelines for Python code.
3. **Pull Request Process**: Clearly describe the changes and their purpose. Ensure that your code has been tested.

## License
- No license.

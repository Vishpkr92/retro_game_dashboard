# Retro Games Collection

A collection of classic arcade-style retro games built with Pygame. This dashboard provides access to four iconic games reimagined with modern programming while maintaining their nostalgic charm.


## Games Included

### 1. Pong
The classic table tennis arcade game. Control your paddle to bounce the ball past your opponent.

**Features:**
- Player vs AI gameplay
- Color-coded paddles (Blue for Player, Red for AI)
- Enhanced ball physics with realistic bouncing
- Score tracking
- First to 5 points wins

**Controls:**
- UP/DOWN arrow keys to move your paddle
- ESC to quit

### 2. Tetris
The iconic block-stacking puzzle game.

**Features:**
- All 7 standard Tetromino shapes
- Next piece preview
- Increasing difficulty as you level up
- Score tracking based on lines cleared
- Hard drop functionality

**Controls:**
- LEFT/RIGHT arrow keys to move pieces
- UP arrow key to rotate
- DOWN arrow key for soft drop
- SPACE for hard drop
- ESC to quit

### 3. Snake
The classic snake game where you grow longer as you eat food.

**Features:**
- Smooth controls
- Increasing speed as the snake grows
- Score tracking
- Game over on collision with self or walls

**Controls:**
- Arrow keys to change direction
- ESC to quit

### 4. Tic-tac-toe
The timeless game of X's and O's.

**Features:**
- Play against AI with three difficulty levels:
  - Easy: Makes random moves
  - Medium: 70% optimal moves, 30% random moves
  - Hard: Uses minimax algorithm for optimal play
- Play against another human player
- Clean visual design
- Win detection and game over screen

**Controls:**
- Mouse click to place X/O
- R to restart after game over
- ESC to return to menu

## Requirements
- Python 3.x
- Pygame library

## Installation

1. Ensure you have Python installed on your system
2. Install the Pygame library:
```bash
pip install pygame
```
or
```bash
sudo apt install python3-pygame  # For Debian/Ubuntu systems
```

## How to Run

Launch the game dashboard:
```bash
python3 retro_game_dashboard.py
```

From the dashboard, click on any game to play. You can return to the dashboard by closing the game window or pressing ESC.

## Technical Details

All games are built using:
- Python 3
- Pygame for graphics and input handling
- Object-oriented programming principles
- Event-driven architecture

The code structure follows a modular approach with separate files for each game, allowing them to be played independently or through the central dashboard.

## Future Enhancements

Planned features for future versions:
- High score tracking and persistence
- Additional games (Breakout, Space Invaders, Pac-Man)
- Customizable controls
- Sound effects and music
- Two-player modes for all games

## Credits

Created by Vishal Phansekar

## License

This project is licensed under the MIT License - see the LICENSE file for details.

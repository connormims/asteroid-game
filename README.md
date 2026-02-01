# Asteroids Game

A classic Asteroids clone built with Python and Pygame. This project features a persistent leaderboard system, smooth physics-based movement, and a retro arcade aesthetic.

## Features
* **Persistent Leaderboard:** High scores are saved to a local JSON file.
* **Username Input:** Enter your initials after each game to track your progress.
* **Arcade Menu:** Toggle between game over stats and top scores.
* **Classic Gameplay:** Physics-based movement, wrap-around screen logic, and asteroid splitting.

## Prerequisites
Before running the game, ensure you have **Python 3.x** installed.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/connormims/asteroid-game.git
   cd asteroid-game


2. **Install Pygame:**
    ```bash
    pip install pygame

## How to Play

* **Launch the game:**
```bash
python main.py

```


## Controls:

* **W / A / D:** Thrust and Rotate
* **Space:** Fire Lasers
* **Enter:** Submit username (on Game Over)
* **R:** Restart Game
* **L:** View Leaderboard
* **B:** Go Back (from Leaderboard)
* **Esc:** Quit Game



## Project Structure

* `main.py`: Main game loop and state management (Playing, Input, Leaderboard).
* `leaderboard.py`: Logic for persistent JSON storage and ranking.
* `player.py`: Player class with rotation and thrust physics.
* `asteroid.py`: Asteroid class with splitting logic.
* `shot.py`: Projectile handling for player lasers.
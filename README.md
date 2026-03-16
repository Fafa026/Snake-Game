# 🐍 Snake Game

A clean Pygame snake game with a high score tracker.

### Start screen
![Start Screen](Start.png)

### Game Over
![Game Over](Game_over.png)

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `↑ ↓ ← →` or `W A S D` | Move snake |
| `R` / `Space` / `Enter` | Restart after game over |

## Features

- **High score tracker** — persisted to `highscore.json` between sessions
- Pulsing food with glow effect
- Smooth snake rendering with directional eyes
- Death flash animation
- Score panel with current score and best score

## Project Structure

```
snake-game/
├── main.py          # Game loop, rendering, state management
├── snake.py         # Snake class (movement, collision, drawing)
├── food.py          # Food class (spawning, pulse animation)
├── requirements.txt
└── README.md
```

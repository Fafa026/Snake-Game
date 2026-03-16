import pygame
import sys
import json
import os
import time
from snake import Snake
from food import Food

#  Constants 
GRID_SIZE   = 20
CELL_SIZE   = 30
WIDTH       = GRID_SIZE * CELL_SIZE
PANEL_H     = 70
HEIGHT      = WIDTH + PANEL_H
FPS         = 60
MOVE_DELAY  = 0.13   # seconds between moves
SCORE_FILE  = "highscore.json"

#   Color Palette 
BG          = (15,  17,  26)
GRID_LINE   = (22,  26,  40)
PANEL_BG    = (10,  12,  20)
SNAKE_HEAD  = (80, 220, 140)
SNAKE_BODY  = (50, 180, 110)
SNAKE_INNER = (40, 150,  90)
SNAKE_EYE   = (10,  30,  20)
FOOD_COL    = (255,  80,  80)
FOOD_GLOW   = (255, 120,  60)
TEXT_MAIN   = (220, 230, 255)
TEXT_DIM    = (90, 100, 140)
ACCENT      = (80, 220, 140)
DANGER      = (255,  80,  80)
OVERLAY_BG  = (10,  12,  20, 210)

SNAKE_COLORS = {
    "head":       SNAKE_HEAD,
    "body":       SNAKE_BODY,
    "body_inner": SNAKE_INNER,
    "eye":        SNAKE_EYE,
}

def load_highscore():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE) as f:
                return json.load(f).get("highscore", 0)
        except Exception:
            pass
    return 0

def save_highscore(score):
    with open(SCORE_FILE, "w") as f:
        json.dump({"highscore": score}, f)

def draw_panel(surface, font_sm, font_lg, score, highscore):
    pygame.draw.rect(surface, PANEL_BG, pygame.Rect(0, 0, WIDTH, PANEL_H))
    pygame.draw.line(surface, GRID_LINE, (0, PANEL_H - 1), (WIDTH, PANEL_H - 1), 1)

    # Score
    lbl = font_sm.render("SCORE", True, TEXT_DIM)
    val = font_lg.render(str(score), True, ACCENT)
    surface.blit(lbl, (24, 10))
    surface.blit(val, (24, 28))

    # High score
    hs_lbl = font_sm.render("BEST", True, TEXT_DIM)
    hs_val = font_lg.render(str(highscore), True, TEXT_MAIN)
    surface.blit(hs_lbl, (WIDTH - 90, 10))
    surface.blit(hs_val, (WIDTH - 90, 28))

    # Title
    title = font_sm.render("SNAKE", True, TEXT_DIM)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 26))

def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_LINE, (x, PANEL_H), (x, HEIGHT), 1)
    for y in range(PANEL_H, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_LINE, (0, y), (WIDTH, y), 1)

def draw_overlay(surface, lines, font_lg, font_sm):
    overlay = pygame.Surface((WIDTH, HEIGHT - PANEL_H), pygame.SRCALPHA)
    overlay.fill(OVERLAY_BG)
    surface.blit(overlay, (0, PANEL_H))
    cy = PANEL_H + (HEIGHT - PANEL_H) // 2 - (len(lines) * 36) // 2
    for text, big, color in lines:
        font = font_lg if big else font_sm
        rendered = font.render(text, True, color)
        surface.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, cy))
        cy += rendered.get_height() + 10

def flash_border(surface, color, alpha):
    border = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(border, (*color, alpha),
                     pygame.Rect(0, PANEL_H, WIDTH, HEIGHT - PANEL_H), 6)
    surface.blit(border, (0, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    try:
        font_lg = pygame.font.SysFont("Consolas", 32, bold=True)
        font_sm = pygame.font.SysFont("Consolas", 14)
        font_xl = pygame.font.SysFont("Consolas", 52, bold=True)
    except Exception:
        font_lg = pygame.font.SysFont(None, 32)
        font_sm = pygame.font.SysFont(None, 18)
        font_xl = pygame.font.SysFont(None, 52)

    snake     = Snake(GRID_SIZE, CELL_SIZE)
    food      = Food(GRID_SIZE, CELL_SIZE)
    highscore = load_highscore()
    score     = 0
    last_move = time.time()
    state     = "start"   # start | playing | dead
    flash_t   = 0.0

    # Offset all game rendering by PANEL_H
    game_surf = pygame.Surface((WIDTH, HEIGHT - PANEL_H))

    while True:
        dt = clock.tick(FPS) / 1000.0
        now = time.time()

        # Events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "start":
                    state = "playing"
                elif state == "dead":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                        snake.reset()
                        food.spawn(set(snake.body))
                        score    = 0
                        last_move = now
                        state    = "playing"
                elif state == "playing":
                    if event.key == pygame.K_UP    or event.key == pygame.K_w:
                        snake.set_direction((0, -1))
                    elif event.key == pygame.K_DOWN  or event.key == pygame.K_s:
                        snake.set_direction((0, 1))
                    elif event.key == pygame.K_LEFT  or event.key == pygame.K_a:
                        snake.set_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.set_direction((1, 0))

        # Game Logic 
        if state == "playing" and now - last_move >= MOVE_DELAY:
            snake.move()
            last_move = now

            if snake.check_wall_collision() or snake.check_self_collision():
                state   = "dead"
                flash_t = now
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
            elif snake.get_head() == food.position:
                snake.grow()
                score += 10
                food.spawn(set(snake.body))

        food.update()

        # Drawing 
        screen.fill(BG)
        draw_panel(screen, font_sm, font_lg, score, highscore)

        # Game area
        game_surf.fill(BG)
        draw_grid(game_surf)
        food.draw(game_surf, FOOD_COL, FOOD_GLOW)
        snake.draw(game_surf, SNAKE_COLORS)
        screen.blit(game_surf, (0, PANEL_H))

        # Death flash border
        if state == "dead":
            age = now - flash_t
            if age < 0.4:
                alpha = int(180 * (1 - age / 0.4))
                flash_border(screen, DANGER, alpha)

        # Overlays
        if state == "start":
            draw_overlay(screen,
                [("SNAKE",      True,  ACCENT),
                 ("press any key", False, TEXT_DIM),
                 ("↑ ↓ ← →  or  W A S D", False, TEXT_DIM)],
                font_xl, font_sm)

        elif state == "dead":
            new_best = score == highscore and score > 0
            lines = [
                ("GAME OVER",     True,  DANGER),
                (f"Score: {score}", False, TEXT_MAIN),
            ]
            if new_best:
                lines.append(("✦ NEW BEST ✦", False, ACCENT))
            lines.append(("[R] Restart", False, TEXT_DIM))
            draw_overlay(screen, lines, font_xl, font_sm)

        pygame.display.flip()

if __name__ == "__main__":
    main()
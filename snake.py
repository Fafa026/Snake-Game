import pygame
from collections import deque

class Snake:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.reset()

    def reset(self):
        cx, cy = self.grid_size // 2, self.grid_size // 2
        self.body = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grew = False

    def set_direction(self, new_dir):
        # Prevent reversing
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.next_direction = new_dir

    def move(self):
        self.direction = self.next_direction
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.appendleft(new_head)
        if not self.grew:
            self.body.pop()
        self.grew = False

    def grow(self):
        self.grew = True

    def get_head(self):
        return self.body[0]

    def check_self_collision(self):
        head = self.body[0]
        return head in list(self.body)[1:]

    def check_wall_collision(self):
        hx, hy = self.body[0]
        return not (0 <= hx < self.grid_size and 0 <= hy < self.grid_size)

    def draw(self, surface, colors):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                               self.cell_size, self.cell_size)
            if i == 0:
                # Head
                pygame.draw.rect(surface, colors["head"], rect, border_radius=6)
                # Eyes
                eye_size = max(3, self.cell_size // 6)
                dx, dy = self.direction
                if dx == 1:
                    eye_positions = [(rect.right - eye_size - 3, rect.top + 5),
                                     (rect.right - eye_size - 3, rect.bottom - eye_size - 5)]
                elif dx == -1:
                    eye_positions = [(rect.left + 3, rect.top + 5),
                                     (rect.left + 3, rect.bottom - eye_size - 5)]
                elif dy == -1:
                    eye_positions = [(rect.left + 5, rect.top + 3),
                                     (rect.right - eye_size - 5, rect.top + 3)]
                else:
                    eye_positions = [(rect.left + 5, rect.bottom - eye_size - 3),
                                     (rect.right - eye_size - 5, rect.bottom - eye_size - 3)]
                for ep in eye_positions:
                    pygame.draw.rect(surface, colors["eye"],
                                     pygame.Rect(ep[0], ep[1], eye_size, eye_size),
                                     border_radius=2)
            else:
                alpha = max(80, 255 - int((i / len(self.body)) * 160))
                color = tuple(min(255, int(c * alpha / 255)) for c in colors["body"])
                inner = rect.inflate(-4, -4)
                pygame.draw.rect(surface, colors["body"], rect, border_radius=4)
                pygame.draw.rect(surface, colors["body_inner"], inner, border_radius=3)
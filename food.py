import pygame
import random
import math

class Food:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.position = (0, 0)
        self.pulse = 0.0
        self.spawn(set())

    def spawn(self, occupied):
        available = [
            (x, y)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
            if (x, y) not in occupied
        ]
        if available:
            self.position = random.choice(available)

    def update(self):
        self.pulse += 0.08
        if self.pulse > 2 * math.pi:
            self.pulse -= 2 * math.pi

    def draw(self, surface, color, glow_color):
        x, y = self.position
        cx = x * self.cell_size + self.cell_size // 2
        cy = y * self.cell_size + self.cell_size // 2

        scale = 1.0 + 0.12 * math.sin(self.pulse)
        radius = int((self.cell_size // 2 - 4) * scale)

        # Glow rings
        for r_offset, alpha in [(radius + 8, 30), (radius + 5, 60)]:
            glow_surf = pygame.Surface((r_offset * 2 + 2, r_offset * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*glow_color, alpha),
                               (r_offset + 1, r_offset + 1), r_offset)
            surface.blit(glow_surf, (cx - r_offset - 1, cy - r_offset - 1))

        # Main circle
        pygame.draw.circle(surface, color, (cx, cy), radius)

        # Shine
        shine_r = max(2, radius // 3)
        shine_pos = (cx - radius // 3, cy - radius // 3)
        pygame.draw.circle(surface, (255, 255, 255), shine_pos, shine_r)
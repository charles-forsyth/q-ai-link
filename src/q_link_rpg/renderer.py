import pygame
import sys
from q_link_rpg.engine.grid_world import GridWorld

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class GameRenderer:
    def __init__(self, width: int, height: int, cell_size: int = 40):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Q-Link RPG")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, grid: GridWorld, episode: int = 0, score: int = 0):
        self.screen.fill(WHITE)
        
        # Draw Grid Lines
        for x in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.screen_width, y))

        # Draw Walls
        for (x, y) in grid.walls:
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, BLACK, rect)

        # Draw Goal
        gx, gy = grid.goal_pos
        rect = pygame.Rect(gx * self.cell_size, gy * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, GREEN, rect)
        
        # Draw Enemies
        for (ex, ey) in grid.enemies:
            rect = pygame.Rect(ex * self.cell_size, ey * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, RED, rect)

        # Draw Hero
        hx, hy = grid.hero_pos
        # Draw hero as a blue circle
        center = (hx * self.cell_size + self.cell_size // 2, hy * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, BLUE, center, self.cell_size // 2 - 2)

        # Draw Info
        text = self.font.render(f"Ep: {episode} Score: {score}", True, BLACK)
        self.screen.blit(text, (5, 5))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def close(self):
        pygame.quit()

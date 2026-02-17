import pygame
import os
from typing import Tuple, Optional
from q_link_rpg.engine.grid_world import GridWorld
from q_link_rpg.engine.game_logic import Action

class GameRenderer:
    CELL_SIZE = 40
    screen: pygame.Surface
    
    # Colors (Forest Theme Fallback)
    COLOR_BG = (34, 139, 34)  # Forest Green
    COLOR_GRID = (50, 100, 50) # Darker Green
    COLOR_HERO = (0, 255, 0)
    COLOR_GOAL = (255, 215, 0)
    COLOR_WALL = (139, 69, 19) # Saddle Brown (Trees/Wood)
    COLOR_ENEMY = (255, 0, 0)

    def __init__(self, grid_width: int, grid_height: int, headless: bool = False):
        self.width = grid_width
        self.height = grid_height
        
        if headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        try:
            pygame.init()
            self.screen = pygame.display.set_mode(
                (self.width * self.CELL_SIZE, self.height * self.CELL_SIZE)
            )
            pygame.display.set_caption("Q-Link RPG - Forest Edition")
        except pygame.error:
            # Fallback for headless environments if explicit flag wasn't set but display failed
            print("Warning: No video device available. Falling back to dummy driver.")
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.init()
            self.screen = pygame.display.set_mode(
                (self.width * self.CELL_SIZE, self.height * self.CELL_SIZE)
            )

        # Load Images
        self.images = {}
        image_dir = os.path.join(os.path.dirname(__file__), "static", "images")
        image_files = {
            "background": "background.png",
            "hero": "agent.png",
            "goal": "goal.png",
            "wall": "obstacle.png", # Trees/Rocks
            "enemy": "enemy.png"
        }
        
        for name, filename in image_files.items():
            path = os.path.join(image_dir, filename)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    if name == "background":
                        # Tile background if needed or stretch? Let's tile.
                        self.images[name] = img
                    else:
                        self.images[name] = pygame.transform.scale(img, (self.CELL_SIZE, self.CELL_SIZE))
                except pygame.error:
                    print(f"Warning: Could not load image {filename}")

    def render(self, grid: GridWorld):
        # Draw Background
        if "background" in self.images:
            # Tile the background
            bg_img = self.images["background"]
            bg_w, bg_h = bg_img.get_size()
            for x in range(0, self.width * self.CELL_SIZE, bg_w):
                for y in range(0, self.height * self.CELL_SIZE, bg_h):
                    self.screen.blit(bg_img, (x, y))
        else:
            self.screen.fill(self.COLOR_BG)

        # Draw Grid (optional on image background, maybe semi-transparent?)
        # Let's keep grid lines for clarity
        for x in range(0, self.width * self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.COLOR_GRID, (x, 0), (x, self.height * self.CELL_SIZE))
        for y in range(0, self.height * self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.COLOR_GRID, (0, y), (self.width * self.CELL_SIZE, y))

        # Draw Walls
        for wall in grid.walls:
            self._draw_cell(wall, self.COLOR_WALL, "wall")

        # Draw Enemies
        for enemy in grid.enemies:
            self._draw_cell(enemy, self.COLOR_ENEMY, "enemy")

        # Draw Goal
        self._draw_cell(grid.goal_pos, self.COLOR_GOAL, "goal")

        # Draw Hero
        self._draw_cell(grid.hero_pos, self.COLOR_HERO, "hero")

        pygame.display.flip()

    def _draw_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int], image_key: Optional[str] = None):
        x, y = pos
        if image_key and image_key in self.images:
            self.screen.blit(self.images[image_key], (x * self.CELL_SIZE, y * self.CELL_SIZE))
        else:
            rect = (
                x * self.CELL_SIZE + 2,
                y * self.CELL_SIZE + 2,
                self.CELL_SIZE - 4,
                self.CELL_SIZE - 4
            )
            pygame.draw.rect(self.screen, color, rect)

    def process_input(self) -> Tuple[Optional[Action], bool]:
        """
        Process Pygame events.
        Returns:
            (action, should_quit): action is the move to make (or None), should_quit is True if window closed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return Action.UP, False
                elif event.key == pygame.K_RIGHT:
                    return Action.RIGHT, False
                elif event.key == pygame.K_DOWN:
                    return Action.DOWN, False
                elif event.key == pygame.K_LEFT:
                    return Action.LEFT, False
                elif event.key == pygame.K_ESCAPE:
                    return None, True
        return None, False

    def close(self):
        pygame.quit()

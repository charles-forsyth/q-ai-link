import random
from enum import IntEnum
from typing import Tuple
from q_link_rpg.engine.grid_world import GridWorld


class Action(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class GameLogic:
    STEP_PENALTY = -1
    WALL_PENALTY = -5
    GOAL_REWARD = 100
    DEATH_PENALTY = -100

    def __init__(self, grid: GridWorld):
        self.grid = grid

    def _move_enemies(self):
        new_enemies = set()
        for ex, ey in self.grid.enemies:
            # Random move: 0=Stay, 1=Up, 2=Right, 3=Down, 4=Left
            move = random.randint(0, 4)
            dx, dy = 0, 0
            if move == 1:
                dy = -1
            elif move == 2:
                dx = 1
            elif move == 3:
                dy = 1
            elif move == 4:
                dx = -1

            nx, ny = ex + dx, ey + dy

            # Check bounds and walls and goal (enemies shouldn't block goal?)
            # Let's say enemies can't walk into walls or goal or other enemies
            if (
                (0 <= nx < self.grid.width and 0 <= ny < self.grid.height)
                and ((nx, ny) not in self.grid.walls)
                and ((nx, ny) != self.grid.goal_pos)
                and ((nx, ny) not in new_enemies)
            ):
                new_enemies.add((nx, ny))
            else:
                new_enemies.add((ex, ey))  # Stay if blocked
        self.grid.enemies = new_enemies

    def step(self, action: Action) -> Tuple[int, bool]:
        """
        Execute an action and return (reward, done).
        """
        # 1. Move Enemies First (or after? let's do before to make it harder/unpredictable)
        self._move_enemies()

        x, y = self.grid.hero_pos

        # Check if enemy moved into hero
        if (x, y) in self.grid.enemies:
            return self.DEATH_PENALTY, True

        dx, dy = 0, 0

        if action == Action.UP:
            dy = -1
        elif action == Action.RIGHT:
            dx = 1
        elif action == Action.DOWN:
            dy = 1
        elif action == Action.LEFT:
            dx = -1

        new_x, new_y = x + dx, y + dy

        # Check bounds
        if not (0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height):
            return self.WALL_PENALTY, False

        # Check walls
        if (new_x, new_y) in self.grid.walls:
            return self.WALL_PENALTY, False

        # Move hero
        self.grid.hero_pos = (new_x, new_y)

        # Check goal
        if (new_x, new_y) == self.grid.goal_pos:
            return self.GOAL_REWARD, True

        # Check enemies again (did hero walk into one?)
        if (new_x, new_y) in self.grid.enemies:
            return self.DEATH_PENALTY, True

        return self.STEP_PENALTY, False

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

    def step(self, action: Action) -> Tuple[int, bool]:
        """
        Execute an action and return (reward, done).
        """
        x, y = self.grid.hero_pos
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

        # Check enemies
        if (new_x, new_y) in self.grid.enemies:
            return self.DEATH_PENALTY, True

        return self.STEP_PENALTY, False

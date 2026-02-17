from typing import List, Tuple, Set


class GridWorld:
    def __init__(
        self,
        width: int,
        height: int,
        start_pos: Tuple[int, int],
        goal_pos: Tuple[int, int],
    ):
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.hero_pos = start_pos
        self.walls: Set[Tuple[int, int]] = set()
        self.enemies: Set[Tuple[int, int]] = set()

    def add_walls(self, walls: List[Tuple[int, int]]) -> None:
        """Add walls to the grid."""
        for wall in walls:
            if wall != self.start_pos and wall != self.goal_pos:
                self.walls.add(wall)

    def add_enemies(self, enemies: List[Tuple[int, int]]) -> None:
        """Add enemies to the grid."""
        for enemy in enemies:
            if enemy != self.start_pos and enemy != self.goal_pos:
                self.enemies.add(enemy)

    def reset(self) -> None:
        """Reset the hero to the start position."""
        self.hero_pos = self.start_pos

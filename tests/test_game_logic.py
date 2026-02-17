import pytest
from q_link_rpg.engine.game_logic import GameLogic, Action
from q_link_rpg.engine.grid_world import GridWorld


@pytest.fixture
def logic():
    grid = GridWorld(5, 5, (0, 0), (4, 4))
    return GameLogic(grid)


def test_valid_move(logic):
    """Test moving the hero into a valid empty cell."""
    # Move Right from (0,0) -> (1,0)
    reward, done = logic.step(Action.RIGHT)
    assert logic.grid.hero_pos == (1, 0)
    assert not done
    assert reward == logic.STEP_PENALTY  # Assuming a small step penalty


def test_wall_collision(logic):
    """Test that moving into a wall keeps the hero in place."""
    logic.grid.add_walls([(1, 0)])
    # Try to move Right into wall at (1,0)
    reward, done = logic.step(Action.RIGHT)

    assert logic.grid.hero_pos == (0, 0)  # Should not move
    assert not done
    assert reward == logic.WALL_PENALTY  # Negative reward for hitting wall


def test_boundary_collision(logic):
    """Test that moving off-grid keeps the hero in place."""
    # Try to move Left from (0,0) -> (-1, 0)
    reward, done = logic.step(Action.LEFT)

    assert logic.grid.hero_pos == (0, 0)
    assert not done
    assert reward == logic.WALL_PENALTY


def test_reach_goal(logic):
    """Test reaching the goal state."""
    logic.grid.hero_pos = (3, 4)  # One step left of goal (4,4)
    reward, done = logic.step(Action.RIGHT)

    assert logic.grid.hero_pos == (4, 4)
    assert done
    assert reward == logic.GOAL_REWARD


def test_enemy_collision(logic):
    """Test colliding with an enemy."""
    logic.grid.add_enemies([(1, 0)])
    reward, done = logic.step(Action.RIGHT)

    assert logic.grid.hero_pos == (
        1,
        0,
    )  # Depending on rules, might move onto enemy or stay?
    # Usually in GridWorld, you move onto the terminal state
    assert done
    assert reward == logic.DEATH_PENALTY

from q_link_rpg.engine.grid_world import GridWorld


def test_grid_initialization(grid_config):
    """Test that the grid is initialized with correct dimensions and entities."""
    grid = GridWorld(
        width=grid_config["width"],
        height=grid_config["height"],
        start_pos=grid_config["start_pos"],
        goal_pos=grid_config["goal_pos"],
    )

    assert grid.width == 10
    assert grid.height == 10
    assert grid.hero_pos == (0, 0)
    assert grid.goal_pos == (9, 9)


def test_add_walls(grid_config):
    """Test adding walls to the grid."""
    grid = GridWorld(10, 10, (0, 0), (9, 9))
    grid.add_walls(grid_config["walls"])

    assert (1, 1) in grid.walls
    assert (2, 2) in grid.walls
    assert (0, 0) not in grid.walls  # Start position should not be a wall


def test_add_enemies(grid_config):
    """Test adding enemies to the grid."""
    grid = GridWorld(10, 10, (0, 0), (9, 9))
    grid.add_enemies(grid_config["enemies"])

    assert (5, 5) in grid.enemies


def test_reset_grid(grid_config):
    """Test resetting the grid state."""
    grid = GridWorld(10, 10, (0, 0), (9, 9))
    grid.hero_pos = (5, 5)  # Move hero manually
    grid.reset()
    assert grid.hero_pos == (0, 0)

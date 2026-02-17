import pytest
import numpy as np
from unittest.mock import MagicMock

# Shared fixtures for testing

@pytest.fixture
def grid_config():
    """Basic grid configuration for a single level."""
    return {
        "width": 10,
        "height": 10,
        "start_pos": (0, 0),
        "goal_pos": (9, 9),
        "walls": [(1, 1), (2, 2)],
        "enemies": [(5, 5)],
        "level_id": 1
    }

@pytest.fixture
def mock_renderer():
    """Mock renderer to test game logic without pygame dependency."""
    renderer = MagicMock()
    renderer.render.return_value = None
    return renderer

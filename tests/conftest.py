import pytest
import numpy as np
from unittest.mock import MagicMock

# Since the source code doesn't exist yet, we will mock or assume the imports will work later.
# For now, we will create dummy classes/fixtures to represent the expected structure if needed,
# or simply rely on the imports to fail (Strict TDD: Red -> Green).
# However, to write meaningful tests, I will assume the structure:
# src.q_link_rpg.engine.grid_world
# src.q_link_rpg.engine.game_logic
# src.q_link_rpg.ai.agent

@pytest.fixture
def grid_config():
    return {
        "width": 10,
        "height": 10,
        "start_pos": (0, 0),
        "goal_pos": (9, 9),
        "walls": [(1, 1), (2, 2)],
        "enemies": [(5, 5)]
    }

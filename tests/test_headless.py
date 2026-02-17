import os
from unittest.mock import patch, MagicMock
from q_link_rpg.renderer import GameRenderer
import pygame


def test_renderer_headless_fallback():
    """Test that GameRenderer falls back to dummy driver if display initialization fails."""
    # Mock pygame.display.set_mode to fail initially, then succeed (after setting dummy)
    with (
        patch("pygame.display.set_mode") as mock_set_mode,
        patch("pygame.display.init"),
        patch("pygame.init") as mock_init,
        patch.dict(os.environ, {}, clear=False),
    ):
        # Simulate failure on first call
        mock_set_mode.side_effect = [
            pygame.error("No available video device"),
            MagicMock(),
        ]

        # We need to make sure pygame.init doesn't actually try to open a window
        mock_init.return_value = (6, 0)

        # Instantiate renderer (grid size 10x10)
        _ = GameRenderer(10, 10, headless=False)

        # Check if SDL_VIDEODRIVER was set to dummy
        assert os.environ.get("SDL_VIDEODRIVER") == "dummy"
        # Check that set_mode was called twice
        assert mock_set_mode.call_count == 2


def test_renderer_explicit_headless():
    """Test that GameRenderer uses dummy driver if explicitly requested."""
    with (
        patch("pygame.display.set_mode") as mock_set_mode,
        patch("pygame.init"),
        patch.dict(os.environ, {}, clear=False),
    ):
        _ = GameRenderer(10, 10, headless=True)

        assert os.environ.get("SDL_VIDEODRIVER") == "dummy"
        assert mock_set_mode.called

import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from q_link_rpg.cli import app
import time

runner = CliRunner()

def test_watch_headless_performance():
    """Verify that watch --headless skips or minimizes sleeps."""
    with (
        patch("q_link_rpg.cli.QLearningAgent") as mock_agent_class,
        patch("q_link_rpg.cli.GameRenderer") as mock_renderer_class,
        patch("time.sleep") as mock_sleep,
        patch("pygame.display.set_mode"),
        patch("pygame.init")
    ):
        # Setup mocks
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        # Simulate agent choosing 0 (UP)
        mock_agent.choose_action.return_value = 0
        
        # Run the command
        result = runner.invoke(app, ["watch", "--episodes", "1", "--headless"])
        
        assert result.exit_code == 0
        
        # Check if any sleep called was >= 0.1 (default delay) or 1.0 (post-episode)
        for call in mock_sleep.call_args_list:
            args, _ = call
            assert args[0] < 0.1, f"Sleep called with {args[0]}, should be bypassed in headless"

def test_watch_gui_retains_sleep():
    """Verify that watch without --headless still sleeps."""
    with (
        patch("q_link_rpg.cli.QLearningAgent") as mock_agent_class,
        patch("q_link_rpg.cli.GameRenderer") as mock_renderer_class,
        patch("time.sleep") as mock_sleep,
        patch("pygame.display.set_mode"),
        patch("pygame.init")
    ):
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        mock_agent.choose_action.return_value = 0
        
        # Mock GameLogic to finish after one step to keep test fast
        with patch("q_link_rpg.cli.create_game") as mock_create:
            mock_grid = MagicMock()
            mock_game = MagicMock()
            mock_game.step.return_value = (10, True) # Done immediately
            mock_create.return_value = (mock_grid, mock_game)
            
            # Run without headless
            result = runner.invoke(app, ["watch", "--episodes", "1"])
            
            assert result.exit_code == 0
            
            # Should have at least one sleep of 1.0 (post-episode)
            sleep_times = [call[0][0] for call in mock_sleep.call_args_list]
            assert 1.0 in sleep_times

from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from q_link_rpg.cli import app
from q_link_rpg.ai.agent import QLearningAgent

runner = CliRunner()


def test_watch_headless_performance(tmp_path):
    """Verify that watch --headless skips or minimizes sleeps."""
    # Create a dummy Q-table file
    save_path = tmp_path / "dummy.npy"
    agent = QLearningAgent((10, 10), 4)
    agent.save(str(save_path))

    with (
        patch("q_link_rpg.cli.QLearningAgent") as mock_agent_class,
        patch("q_link_rpg.cli.GameRenderer") as mock_renderer_class,
        patch("time.sleep") as mock_sleep,
        patch("pygame.display.set_mode"),
        patch("pygame.init"),
    ):
        # Setup mocks
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        # Simulate agent choosing 0 (UP)
        mock_agent.choose_action.return_value = 0

        # Configure renderer
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer
        mock_renderer.process_input.return_value = (None, False)

        # Run the command with headless flag
        result = runner.invoke(
            app,
            ["watch", "--load-path", str(save_path), "--episodes", "1", "--headless"],
        )

        assert result.exit_code == 0

        # Check if any sleep called was >= 0.1 (default delay) or 0.5 (post-episode)
        # Headless should bypass delay and post-episode sleep
        for call in mock_sleep.call_args_list:
            args, _ = call
            assert args[0] < 0.1, (
                f"Sleep called with {args[0]}, should be bypassed in headless"
            )


def test_watch_gui_retains_sleep(tmp_path):
    """Verify that watch without --headless still sleeps."""
    # Create a dummy Q-table file
    save_path = tmp_path / "dummy.npy"
    agent = QLearningAgent((10, 10), 4)
    agent.save(str(save_path))

    with (
        patch("q_link_rpg.cli.QLearningAgent") as mock_agent_class,
        patch("q_link_rpg.cli.GameRenderer") as mock_renderer_class,
        patch("time.sleep") as mock_sleep,
        patch("pygame.display.set_mode"),
        patch("pygame.init"),
    ):
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        mock_agent.choose_action.return_value = 0

        # Configure renderer
        mock_renderer = MagicMock()
        mock_renderer_class.return_value = mock_renderer
        mock_renderer.process_input.return_value = (None, False)

        # Mock GameLogic to finish after one step to keep test fast
        with patch("q_link_rpg.cli.GameLogic") as mock_logic_class:
            mock_logic = MagicMock()
            mock_logic_class.return_value = mock_logic
            mock_logic.step.return_value = (10, True)  # Done immediately

            # Run without headless
            result = runner.invoke(
                app, ["watch", "--load-path", str(save_path), "--episodes", "1"]
            )

            assert result.exit_code == 0

            # Should have at least one sleep of 0.5 (post-episode) or delay
            sleep_times = [call[0][0] for call in mock_sleep.call_args_list]
            # In cli.py: delay default 0.1, post-episode 0.5
            # Since step returns done=True immediately, we might miss 0.1 delay if loop breaks?
            # Wait, logic:
            # while not done:
            #   ...
            #   reward, done = logic.step(action)
            #   time.sleep(delay)
            # So if done becomes True, we still sleep delay once.

            assert 0.5 in sleep_times or 0.1 in sleep_times

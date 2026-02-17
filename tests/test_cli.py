from typer.testing import CliRunner
from q_link_rpg.cli import app
from q_link_rpg.ai.agent import QLearningAgent
import os

runner = CliRunner()

def test_train_command(tmp_path):
    save_path = tmp_path / "test_q_table.npy"
    result = runner.invoke(app, ["train", "--episodes", "10", "--save-path", str(save_path)])
    assert result.exit_code == 0
    assert "Training complete" in result.output
    assert os.path.exists(save_path)

def test_watch_command_missing_file():
    result = runner.invoke(app, ["watch", "--load-path", "non_existent_file.npy"])
    assert "Error: Q-table file" in result.output
    assert result.exit_code == 0

def test_watch_command_success(tmp_path, mocker):
    # Mock renderer to avoid GLX errors and window popup
    mock_renderer = mocker.patch("q_link_rpg.cli.GameRenderer")
    
    # Create a dummy Q-table
    save_path = tmp_path / "dummy_q_table.npy"
    agent = QLearningAgent((10, 10), 4)
    agent.save(str(save_path))
    
    result = runner.invoke(app, ["watch", "--load-path", str(save_path), "--episodes", "1", "--delay", "0.0"])
    assert result.exit_code == 0
    assert "Starting Episode 1" in result.output
    assert "Episode 1 Finished" in result.output
    assert mock_renderer.called

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "human" in result.output
    assert "train" in result.output
    assert "watch" in result.output

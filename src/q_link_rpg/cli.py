import typer
import time
import os
import random
import numpy as np
from pathlib import Path
from q_link_rpg.engine.grid_world import GridWorld
from q_link_rpg.engine.game_logic import GameLogic, Action
from q_link_rpg.ai.agent import QLearningAgent
from q_link_rpg.renderer import GameRenderer
from typing import Optional

app = typer.Typer()

def create_level(level_id: int) -> GridWorld:
    if level_id == 1:
        grid = GridWorld(10, 10, (0, 0), (9, 9))
    elif level_id == 2:
        grid = GridWorld(10, 10, (0, 0), (9, 9))
        grid.add_walls([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    elif level_id == 3:
        grid = GridWorld(10, 10, (0, 0), (9, 9))
        grid.add_enemies([(5, 5), (6, 6)])
    elif level_id == 4:
        grid = GridWorld(15, 15, (0, 0), (14, 14))
        # Simple walls
        for i in range(2, 13):
            grid.add_walls([(i, 5)])
    elif level_id == 5:
        grid = GridWorld(15, 15, (0, 0), (14, 14))
        # Walls and enemies
        for i in range(2, 13):
            grid.add_walls([(5, i)])
        grid.add_enemies([(8, 8), (9, 9), (10, 10)])
    elif level_id == 6:
        grid = GridWorld(20, 20, (0, 0), (19, 19))
        # Larger grid, scattered walls
        import random
        random.seed(42) # Fixed seed for reproducibility
        for _ in range(30):
            x, y = random.randint(0, 19), random.randint(0, 19)
            if (x, y) not in [(0, 0), (19, 19)]:
                grid.add_walls([(x, y)])
    elif level_id == 7:
        grid = GridWorld(10, 10, (0, 0), (9, 9))
        # Enemy swarm
        grid.add_enemies([(i, j) for i in range(3, 8) for j in range(3, 8) if (i+j)%2 == 0])
    elif level_id == 8:
        grid = GridWorld(20, 20, (0, 0), (19, 19))
        # Open field, few enemies
        grid.add_enemies([(5, 5), (15, 15), (5, 15), (15, 5)])
    elif level_id == 9:
        grid = GridWorld(15, 15, (0, 0), (14, 14))
        # Corridor
        for y in range(15):
            if y != 7:
                grid.add_walls([(5, y), (9, y)])
    elif level_id == 10:
        grid = GridWorld(20, 20, (0, 0), (19, 19))
        # Maze-like (simple checkerboard pattern for now)
        for x in range(20):
            for y in range(20):
                if (x + y) % 2 == 1 and (x, y) not in [(0, 0), (19, 19)]:
                     if random.random() < 0.3:
                         grid.add_walls([(x, y)])
    else:
        raise ValueError(f"Invalid level ID: {level_id}")
    return grid

@app.command()
def train(episodes: int = 1000, level: int = 1, save_path: str = typer.Option("q_table.npy", "--save-path")):
    """
    Train a Q-Learning agent on a specific level.
    """
    try:
        grid = create_level(level)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    logic = GameLogic(grid)
    # Action space size is len(Action) which is 4
    agent = QLearningAgent((grid.width, grid.height), len(Action))

    for episode in range(episodes):
        state = grid.hero_pos
        done = False
        steps = 0
        max_steps = 1000
        while not done and steps < max_steps:
            steps += 1
            action_idx = agent.choose_action(state, epsilon=0.1)
            action = Action(action_idx)
            
            reward, done = logic.step(action)
            next_state = grid.hero_pos
            
            agent.learn(state, action_idx, reward, next_state, done)
            state = next_state
        
        if (episode + 1) % 100 == 0:
            typer.echo(f"Episode {episode + 1}/{episodes} completed.")
        
        grid.reset()

    agent.save(save_path)
    typer.echo(f"Training complete. Q-table saved to {save_path}")

@app.command()
def watch(load_path: str = typer.Option(..., "--load-path"), episodes: int = 5, level: int = 1, delay: float = 0.1, headless: bool = False):
    """
    Watch a trained agent play on a specific level.
    """
    if not os.path.exists(load_path):
        typer.echo(f"Error: Q-table file not found at {load_path}")
        raise typer.Exit(code=1)

    try:
        grid = create_level(level)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    logic = GameLogic(grid)
    agent = QLearningAgent((grid.width, grid.height), len(Action))
    try:
        agent.load(load_path)
    except Exception as e:
        typer.echo(f"Error loading Q-table: {e}")
        raise typer.Exit(code=1)

    renderer = GameRenderer(grid.width, grid.height, headless=headless)

    try:
        for episode in range(episodes):
            typer.echo(f"Starting Episode {episode + 1}")
            grid.reset()
            state = grid.hero_pos
            done = False
            steps = 0
            max_steps = 1000
            
            while not done and steps < max_steps:
                steps += 1
                # Process input to keep window responsive and check for quit
                _, should_quit = renderer.process_input()
                if should_quit:
                    typer.echo("Watch mode interrupted by user.")
                    return

                renderer.render(grid)
                
                # Agent chooses action (pure exploitation)
                action_idx = agent.choose_action(state, epsilon=0.0)
                action = Action(action_idx)
                
                reward, done = logic.step(action)
                state = grid.hero_pos
                
                if not headless:
                    time.sleep(delay)
            
            renderer.render(grid)
            typer.echo(f"Episode {episode + 1} Finished")
            if not headless:
                time.sleep(0.5)
            
    finally:
        renderer.close()

@app.command()
def human(level: int = 1):
    """
    Play the game manually using arrow keys.
    """
    try:
        grid = create_level(level)
    except ValueError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    logic = GameLogic(grid)
    renderer = GameRenderer(grid.width, grid.height)

    try:
        done = False
        while not done:
            renderer.render(grid)
            
            action, should_quit = renderer.process_input()
            if should_quit:
                typer.echo("Game quit by user.")
                break
            
            if action is not None:
                reward, done = logic.step(action)
                if done:
                    renderer.render(grid)
                    if reward > 0:
                        typer.echo(f"You Win! Reward: {reward}")
                    else:
                        typer.echo(f"Game Over! Reward: {reward}")
                    time.sleep(2.0)
            
            # Small delay to limit CPU usage
            time.sleep(0.01)

    finally:
        renderer.close()

if __name__ == "__main__":
    app()

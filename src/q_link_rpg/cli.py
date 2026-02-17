import typer
import time
import pygame
from q_link_rpg.engine.grid_world import GridWorld
from q_link_rpg.engine.game_logic import GameLogic, Action
from q_link_rpg.ai.agent import QLearningAgent
from q_link_rpg.renderer import GameRenderer

app = typer.Typer()

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
START_POS = (0, 0)
GOAL_POS = (9, 9)
WALLS = [(1, 1), (1, 2), (2, 2), (5, 5), (6, 5), (7, 5), (3, 7), (4, 7), (5, 7)]
ENEMIES = [(3, 3), (4, 4), (6, 2), (8, 7)]


def create_game():
    grid = GridWorld(DEFAULT_WIDTH, DEFAULT_HEIGHT, START_POS, GOAL_POS)
    grid.add_walls(WALLS)
    grid.add_enemies(ENEMIES)
    game = GameLogic(grid)
    return grid, game


@app.command()
def human(
    headless: bool = typer.Option(
        False, "--headless", help="Run in headless mode (no window)"
    ),
):
    """Play the game manually."""
    grid, game = create_game()
    renderer = GameRenderer(DEFAULT_WIDTH, DEFAULT_HEIGHT, headless=headless)

    running = True
    while running:
        action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    action = Action.UP
                elif event.key == pygame.K_RIGHT:
                    action = Action.RIGHT
                elif event.key == pygame.K_DOWN:
                    action = Action.DOWN
                elif event.key == pygame.K_LEFT:
                    action = Action.LEFT

        if action is not None:
            reward, done = game.step(action)
            renderer.draw(grid, score=reward)
            if done:
                print(f"Game Over! Reward: {reward}")
                time.sleep(1)
                grid.reset()
                renderer.draw(grid)  # Redraw reset state

        renderer.draw(grid)
        time.sleep(0.01)  # Small delay to reduce CPU usage

    renderer.close()


@app.command()
def train(
    episodes: int = 1000,
    save_path: str = "q_table.npy",
    epsilon: float = 1.0,
    decay: float = 0.995,
    min_epsilon: float = 0.01,
):
    """Train the Q-Learning agent."""
    grid, game = create_game()
    agent = QLearningAgent((DEFAULT_WIDTH, DEFAULT_HEIGHT), 4)  # 4 actions

    for episode in range(episodes):
        grid.reset()
        state = grid.hero_pos
        done = False
        total_reward = 0

        while not done:
            action_idx = agent.choose_action(state, epsilon)
            action = Action(action_idx)

            reward, done = game.step(action)
            next_state = grid.hero_pos

            agent.learn(state, action_idx, reward, next_state, done)

            state = next_state
            total_reward += reward

        epsilon = max(min_epsilon, epsilon * decay)

        if episode % 100 == 0:
            print(
                f"Episode {episode}: Total Reward: {total_reward}, Epsilon: {epsilon:.2f}"
            )

    agent.save(save_path)
    print(f"Training complete. Q-table saved to {save_path}")


@app.command()
def watch(
    load_path: str = "q_table.npy",
    episodes: int = 5,
    delay: float = 0.1,
    headless: bool = typer.Option(
        False, "--headless", help="Run in headless mode (no window)"
    ),
):
    """Watch the trained agent play."""
    grid, game = create_game()
    agent = QLearningAgent((DEFAULT_WIDTH, DEFAULT_HEIGHT), 4)
    try:
        agent.load(load_path)
    except FileNotFoundError:
        print(f"Error: Q-table file '{load_path}' not found. Train first!")
        return

    renderer = GameRenderer(DEFAULT_WIDTH, DEFAULT_HEIGHT, headless=headless)

    for episode in range(episodes):
        grid.reset()
        state = grid.hero_pos
        done = False
        total_reward = 0
        print(f"Starting Episode {episode + 1}...")

        while not done:
            renderer.handle_events()
            action_idx = agent.choose_action(state, epsilon=0.0)  # Greedy
            action = Action(action_idx)

            reward, done = game.step(action)
            state = grid.hero_pos
            total_reward += reward

            renderer.draw(grid, episode=episode + 1, score=total_reward)
            time.sleep(delay)

        print(f"Episode {episode + 1} Finished. Total Reward: {total_reward}")
        time.sleep(1)

    renderer.close()


if __name__ == "__main__":
    app()

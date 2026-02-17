import numpy as np
from typing import Tuple
from q_link_rpg.ai.persistence import save_q_table, load_q_table


class QLearningAgent:
    def __init__(
        self,
        state_space_size: Tuple[int, int],
        action_space_size: int,
        alpha: float = 0.1,
        gamma: float = 0.9,
    ):
        self.state_space_size = state_space_size
        self.action_space_size = action_space_size
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        # Initialize Q-table with zeros
        # Shape: (*state_space_size, action_space_size) -> (width, height, actions)
        self.q_table = np.zeros(state_space_size + (action_space_size,))

    def choose_action(self, state: Tuple[int, int], epsilon: float) -> int:
        """
        Choose an action using epsilon-greedy policy.
        """
        if np.random.random() < epsilon:
            return np.random.randint(self.action_space_size)
        else:
            return int(np.argmax(self.q_table[state]))

    def learn(
        self,
        state: Tuple[int, int],
        action: int,
        reward: float,
        next_state: Tuple[int, int],
        done: bool,
    ) -> None:
        """
        Update Q-value based on the action taken and the reward received.
        """
        old_value = self.q_table[state + (action,)]
        next_max = np.max(self.q_table[next_state])

        if done:
            # If done, there is no next state value (or it's terminal 0)
            # Actually, standard Q-learning uses the reward as the target for terminal states
            target = reward
        else:
            target = reward + self.gamma * next_max

        new_value = old_value + self.alpha * (target - old_value)
        self.q_table[state + (action,)] = new_value

    def save(self, path: str) -> None:
        """Save the Q-table to a file."""
        save_q_table(self.q_table, path)

    def load(self, path: str) -> None:
        """Load the Q-table from a file."""
        self.q_table = load_q_table(path)

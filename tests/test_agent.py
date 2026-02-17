import pytest
import numpy as np
import os
from q_link_rpg.ai.agent import QLearningAgent
from q_link_rpg.engine.game_logic import Action

@pytest.fixture
def agent():
    # 5x5 grid, 4 actions
    state_space_size = (5, 5) 
    action_space_size = 4
    return QLearningAgent(state_space_size, action_space_size)

def test_agent_initialization(agent):
    """Test Q-table initialization."""
    assert agent.q_table.shape == (5, 5, 4)
    assert np.all(agent.q_table == 0.0)

def test_choose_action_greedy(agent):
    """Test greedy action selection (exploitation)."""
    # Set a high Q-value for action 2 (DOWN) at state (0,0)
    agent.q_table[0, 0, 2] = 10.0
    action = agent.choose_action((0, 0), epsilon=0.0) # Full exploitation
    assert action == 2 # Should choose the action with highest Q-value

def test_learn_update(agent):
    """Test the Q-learning update rule."""
    state = (0, 0)
    action = 1 # RIGHT
    reward = 10.0
    next_state = (1, 0)
    done = False
    
    initial_q = agent.q_table[0, 0, 1]
    agent.learn(state, action, reward, next_state, done)
    
    # Q_new = Q_old + alpha * (reward + gamma * max(Q_next) - Q_old)
    # With 0 initialization: Q_new = 0 + 0.1 * (10 + 0.9 * 0 - 0) = 1.0
    # Assuming alpha=0.1, gamma=0.9
    updated_q = agent.q_table[0, 0, 1]
    assert updated_q > initial_q

def test_save_load_q_table(agent, tmp_path):
    """Test saving and loading the Q-table."""
    # Modify Q-table
    agent.q_table[0, 0, 0] = 5.5
    
    save_path = tmp_path / "q_table.npy"
    agent.save(save_path)
    
    assert os.path.exists(save_path)
    
    new_agent = QLearningAgent((5, 5), 4)
    new_agent.load(save_path)
    
    assert new_agent.q_table[0, 0, 0] == 5.5
    np.testing.assert_array_equal(agent.q_table, new_agent.q_table)

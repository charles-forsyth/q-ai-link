# 🤖 Q-Link RPG: Q-Learning Grid World

[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-brightgreen)](https://github.com/ucr-research-computing/q-ai-link)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated 2D tile-based Grid World environment designed for training and visualizing reinforcement learning agents. Built with **Pygame** for the engine and **FastAPI** for the web interface, Q-Link RPG bridges the gap between CLI-based training and interactive web visualization.

---

## 🚀 Overview

Q-Link RPG is a research-oriented game engine where an AI agent (Hero) learns to navigate a hazardous grid to reach a goal (Data Node). The agent utilizes **Q-Learning** to find the optimal path while avoiding firewalls (walls) and glitches (enemies).

### Key Features
- **Hybrid Interface:** Seamlessly switch between CLI for high-speed training and Web for intuitive visualization.
- **Advanced AI:** Implement and observe a Q-Learning agent with persistence (Save/Load Q-Tables).
- **Manual Mode:** Play as the hero yourself using keyboard controls.
- **Dynamic Levels:** 10+ pre-configured levels ranging from open fields to complex mazes.
- **Modern Stack:** Powered by `uv`, `fastapi`, `numpy`, and `pygame`.

---

## 🏗️ Architecture

The system is modularly designed to separate the game engine from the visualization and AI layers:

- **`q_link_rpg.engine`**: The core logic, handling grid physics, collisions, and state transitions.
- **`q_link_rpg.ai`**: The Q-Learning implementation and persistence logic.
- **`q_link_rpg.renderer`**: A headless-compatible Pygame renderer.
- **`q_link_rpg.web`**: A FastAPI-based REST API and SPA for web-based interaction.

---

## 🛠️ Installation

This project uses `uv` for ultra-fast dependency management.

```bash
# Clone the repository
git clone https://github.com/ucr-research-computing/q-ai-link.git
cd q-ai-link

# Install dependencies and sync environment
uv sync
```

---

## 🎮 Usage

### CLI Interface
The `q-link` command provides a unified entry point:

#### 1. Manual Play
Test the mechanics yourself:
```bash
uv run q-link human --level 2
```

#### 2. Training the Agent
Train the Q-Learning model on a specific level:
```bash
uv run q-link train --episodes 2000 --level 5 --save-path models/my_q_table.npy
```

#### 3. Watch the Agent
Observe a trained agent in action:
```bash
uv run q-link watch --load-path q_table.npy --level 5
```

### Web Interface
Launch the web server to interact with the game in your browser:
```bash
uv run uvicorn q_link_rpg.web:app --reload
```
Navigate to `http://localhost:8000` to play or watch the agent.

---

## 🧪 Development & Testing

We maintain a rigorous testing suite using `pytest`:

```bash
# Run all tests
uv run pytest

# Run with coverage (optional)
uv run pytest --cov=src
```

### Skywalker Development Workflow
This project follows the **Skywalker Workflow**:
1. **Branch & Bump:** Create feature branches and bump version in `pyproject.toml`.
2. **The Local Gauntlet:** Run `ruff` and `pytest` iteratively.
3. **PR & Audit:** Use GitHub CLI for PRs and code audits.

---

## 🎨 Assets
All visual assets were generated using AI-native design principles:
- **Agent:** Neural avatar representing the Q-Learning process.
- **Goal:** The "Data Node" target.
- **Obstacles:** Firewall blocks and Glitch enemies.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by the UCR Research Computing Team.*

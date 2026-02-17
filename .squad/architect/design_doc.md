# Design Document: q-link-rpg

## Mission Overview
Create a 2D tile-based Grid World game called `q-link-rpg` where a Q-Learning agent learns to navigate to a goal while avoiding enemies. The game features a **Forest Theme** and supports **multiple levels** with increasing difficulty.

## Tech Stack
- **Language:** Python 3.12+
- **Dependency Management:** `uv`
- **Game Engine:** `pygame` (Logic separated for headless support)
- **Math/AI:** `numpy` (Q-table management)
- **CLI Framework:** `typer` or `argparse`
- **Quality Assurance:**
  - **Linting/Formatting:** `ruff`
  - **Type Checking:** `mypy`
  - **Testing:** `pytest`

## Architectural Design

### 1. Core Engine (`src/q_link_rpg/engine/`)
- **`GridWorld`**: Manages the state of the game.
  - **Level Management**: Support for loading multiple level layouts (e.g., from JSON/text files or procedurally generated).
  - **Entities**: Hero, Walls (Trees/Rocks), Enemies (Forest Creatures), Goal.
- **`GameLogic`**: Handles movement rules, collision detection, and reward calculation.
- **`Renderer`**: Pygame implementation with a **Forest Theme**.
  - **Assets**: Use forest-themed sprites/tiles (trees, grass, paths) instead of abstract squares.

### 2. AI Agent (`src/q_link_rpg/ai/`)
- **`QLearningAgent`**: Implements tabular Q-learning.
- **State Representation**: Coordinate-based state `(hero_x, hero_y, enemy_positions, level_id)`.
- **Action Space**: Up, Down, Left, Right.
- **Persistence**: Save/Load Q-table using `numpy.save` / `numpy.load`.

### 3. CLI Interface (`src/q_link_rpg/cli.py`)
- `q-link human`: Manual control via arrow keys.
  - Supports level progression (completing a level advances to the next).
- `q-link train --episodes N --level <ID>`: Train the agent on a specific level or all levels.
- `q-link watch --level <ID>`: Watch the trained agent play a specific level.

## Data Safety & Persistence
- The **Gatekeeper** will audit `agent_persistence.py` to ensure that loaded Q-tables are validated and do not contain malicious code.

## Toolchain & Commands
- **Install:** `uv sync`
- **Lint:** `uv run ruff check .`
- **Format:** `uv run ruff format .`
- **Type Check:** `uv run mypy src`
- **Test:** `uv run pytest`

## CI/CD Strategy
- GitHub Actions will run the "Local Gauntlet" on every push to `feature/*` branches.
- Successful UAT (User Acceptance Testing) in headless mode is required for merging.

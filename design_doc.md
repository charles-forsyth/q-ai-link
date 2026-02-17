# Design Doc: Web Interface for Q-Link RPG

## Objective
Transform the existing CLI-based Q-Learning RPG into a web application to improve accessibility and visualization.

## Architecture
1.  **Backend (Python/FastAPI):**
    *   Expose the existing `GameEngine` and `QTable` via REST endpoints.
    *   Endpoints:
        *   `GET /state`: Returns current grid, agent position, and score.
        *   `POST /action`: Accepts an action (move), updates state, returns new state.
        *   `POST /reset`: Resets the game episode.
    *   Serve static assets (images, CSS, JS).

2.  **Frontend (HTML/JS):**
    *   Simple Single Page Application (SPA).
    *   Canvas or Grid-based rendering using the generated assets.
    *   Keyboard controls for manual play; "Auto" button for Q-learning agent.

3.  **Assets (Nano Banana):**
    *   **Background:** Cyberpunk/Circuitry theme.
    *   **Agent:** Robot/AI avatar.
    *   **Goal:** Glowing data node or portal.
    *   **Obstacle:** Firewall or glitch block.

## Toolchain
*   **Web Framework:** `fastapi`, `uvicorn`
*   **Template Engine:** `jinja2` (for initial page load)
*   **Package Manager:** `uv`

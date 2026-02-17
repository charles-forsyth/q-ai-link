# Design Doc: Fix GLX Errors (Headless Support)

## Problem
The `q-link-rpg` application uses Pygame for rendering. In environments without an X server or valid GLX configuration (e.g., CI/CD pipelines, remote servers via SSH), calling `pygame.display.set_mode()` or `pygame.init()` fails with GLX errors or "No available video device".

## Objective
Enable the application to run in headless mode by falling back to a dummy video driver when a display is unavailable.

## Strategy
1.  **Auto-detection & Fallback:** Modify `GameRenderer` to attempt to initialize the display. If it fails, set `SDL_VIDEODRIVER=dummy` and retry.
2.  **CLI Support:** Add an optional `--headless` flag to the CLI to explicitly force headless mode.

## Technical Implementation (Python/Pygame)

### `src/q_link_rpg/renderer.py`
- In `GameRenderer.__init__`, check for an existing display or try to initialize.
- Use a try-except block around `pygame.display.set_mode()`.
- If `pygame.error` is caught, set `os.environ["SDL_VIDEODRIVER"] = "dummy"` and re-initialize.
- Log a warning when falling back to dummy mode.

### `src/q_link_rpg/cli.py`
- Add `--headless` option to `human` and `watch` commands using Typer.
- Pass the `headless` flag to `GameRenderer`.

## Testing Plan
1.  **Unit Test:** Mock Pygame initialization to simulate failure and verify the fallback logic in `GameRenderer`.
2.  **Functional Test:** Run the application with `SDL_VIDEODRIVER=dummy` set externally and verify it starts without error.

## Toolchain
- **Language:** Python 3.12+
- **Project Manager:** `uv`
- **Lint/Format:** `ruff`
- **Test:** `pytest`

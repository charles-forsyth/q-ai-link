# Design Doc: Optimize Headless Mode for Speed

## Problem
Headless mode is intended for automated testing and CI/CD environments. However, the `watch` command currently respects the same `delay` and post-episode `time.sleep(1)` as the visual mode, making headless runs unnecessarily slow.

## Objective
Automatically bypass or minimize execution delays when the `--headless` flag is used, enabling faster verification.

## Strategy
1.  **Conditional Delay:** In the `watch` command, set `delay = 0` if `headless` is true, unless the user explicitly provided a non-default delay (actually, if they want it headless, they probably want it fast).
2.  **Bypass Post-Episode Sleep:** Skip the `time.sleep(1)` after an episode finishes if `headless` is true.
3.  **Engine Optimization:** Ensure the renderer's `draw` calls in headless mode are as lightweight as possible (which they should be with the dummy driver, but we should verify).

## Technical Implementation (Python)

### `src/q_link_rpg/cli.py`
- Modify `watch` command:
    - If `headless` is `True`, force `delay` to `0.0` (or a very small value) and skip the final `time.sleep(1)`.
- Modify `human` command:
    - Similarly skip `time.sleep` in headless if applicable.

## Testing Plan
1.  **Unit Test:** Verify that `time.sleep` is not called with non-zero values during a headless `watch` run (using mocks).
2.  **Functional Test:** Measure the execution time of `uv run q-link watch --episodes 1 --headless`. It should be near-instant.

## Toolchain
- **Language:** Python 3.12+
- **Project Manager:** `uv`
- **Lint/Format:** `ruff`
- **Test:** `pytest`

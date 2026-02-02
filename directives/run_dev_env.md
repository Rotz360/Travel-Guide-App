# Run Development Environment

**Goal**: Start the Travel Guide App development environment (Backend + Frontend).

## Inputs
- None

## Execution Tools
- `execution/run_dev_env.py`

## Output
- Running servers on `http://localhost:8000` (Backend) and `http://localhost:3000` (Frontend).

## Steps
1.  **Check Ports**: Ensure ports 8000 and 3000 are explicitly available.
2.  **Execute Script**: Run `python execution/run_dev_env.py`.
3.  **Verify**: Open `http://localhost:3000` in the browser.

## Error Handling
- **Ports in use**: If ports are busy, the script should fail gracefully and suggest freeing them.
- **Dependencies missing**: If `npm` or `python` fails, prompt to install dependencies.

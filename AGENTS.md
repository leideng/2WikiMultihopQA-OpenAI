# Repository Guidelines

## Project Structure & Module Organization
`main.py` is the core evaluator: it loads `data/2wikimqa_200_samples_from_blend.json`, sends batched OpenAI-compatible chat requests, and writes per-sample metrics to `results/*.csv`. Use `test.py` and `test-qwen3-8b.py` for simple endpoint smoke checks. Keep dataset inputs in `data/` and generated benchmark outputs in `results/`. `eval-qwen3-8b.sh` is a convenience wrapper for one model-specific run.

## Build, Test, and Development Commands
Install dependencies with:

```bash
uv sync
```

Run the evaluator with defaults:

```bash
uv run python main.py
```

Run without API calls for a fast sanity check:

```bash
uv run python main.py --debug-mode --max-samples 5
```

Smoke-test an OpenAI-compatible endpoint:

```bash
uv run python test.py
```

Use `uv run python test-qwen3-8b.py` or `bash eval-qwen3-8b.sh` when validating the Qwen path.

## Coding Style & Naming Conventions
Target Python 3.11+ and follow the existing script-oriented style in `main.py`: 4-space indentation, `snake_case` for functions and variables, and uppercase `DEFAULT_*` constants for CLI defaults. Keep CLI flags descriptive and hyphenated, matching the current argparse pattern such as `--save-results-path`. Prefer small helper functions over inline metric or prompt logic when extending the evaluator.

## Testing Guidelines
There is no formal `pytest` suite yet; validation is currently script-based. Before submitting changes, run `uv run python main.py --debug-mode --max-samples 5` to verify argument parsing, batching, and CSV writing. For endpoint changes, also run the relevant smoke test script with `OPENAI_API_KEY` and `OPENAI_BASE_URL` set. Name any new quick-check scripts `test-<model>.py` or similarly explicit filenames.

## Commit & Pull Request Guidelines
Recent history uses short, imperative subjects such as `add qwen3-8b results` and `disable thinking in vllm for qwen3`. Keep commits focused and concise, one change per commit. Pull requests should state which model or evaluation path changed, list the commands run, and note any new output files under `results/`. Include sample metrics or screenshots only when they clarify behavior.

## Configuration Tips
Set `OPENAI_API_KEY` and `OPENAI_BASE_URL` before any non-debug run. Avoid committing secrets, large temporary datasets, or ad hoc result files unless they are intentional benchmark artifacts.

# Repository Guidelines

## Project Structure & Module Organization
`main.py` is the evaluator entry point. It reads a dataset from `data/`, sends async OpenAI-compatible chat requests, and writes CSV metrics to `results/`. Use `fix_2wikimqa_no_answers.py` to regenerate the corrected datasets: `data/2wikimqa_200_samples_from_blend_fix.json` and `data/2wikimqa_200_samples_from_blend_filter.json`. Keep smoke-test scripts at the repo root, following the existing pattern in `test.py` and `test-qwen3-8b.py`.

## Build, Test, and Development Commands
Install dependencies with `uv sync`. Run the default evaluation with `uv run python main.py`; this currently uses the filtered dataset and writes to `results/2wikimqa_200_samples_from_blend_filter/`. For a fast local check, run `uv run python main.py --debug-mode --max-samples 5`. Regenerate corrected datasets with `python fix_2wikimqa_no_answers.py`. Validate endpoint connectivity with `uv run python test.py` or `uv run python test-qwen3-8b.py`.

## Coding Style & Naming Conventions
Target Python 3.11+ and match the current script style: 4-space indentation, `snake_case` for functions and variables, and uppercase `DEFAULT_*` constants for CLI defaults and paths. Keep argument names explicit and hyphenated, such as `--eval-dataset-path` and `--save-results-path`. When adding data-processing logic, prefer small helper functions over expanding `main()` inline.

## Testing Guidelines
This repo does not use `pytest`; verification is script-based. Before submitting changes, run the debug evaluator path and, if relevant, regenerate datasets to confirm output files and counts. For endpoint-related changes, run the appropriate smoke test with `OPENAI_API_KEY` and `OPENAI_BASE_URL` set. Name any new ad hoc validation scripts clearly, for example `test-<model>.py`.

## Commit & Pull Request Guidelines
Recent commits use short imperative subjects. Keep commits atomic and descriptive; `docs: refresh README for corrected datasets` is the right level of specificity. Pull requests should state which dataset variant or result directory is affected, list the commands you ran, and note whether generated JSON or CSV artifacts were intentionally updated.

## Configuration Tips
Never commit secrets. Treat files under `results/` as generated artifacts and only keep them when they represent intentional benchmark outputs.

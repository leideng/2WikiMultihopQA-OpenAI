# Getting Started

## Requirements

- Python `>= 3.11`
- `uv`
- An OpenAI-compatible API endpoint
- Environment variables:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`

The evaluator reads credentials from the environment in `main.py`. If either variable is missing and `--debug-mode` is not enabled, execution stops with an error.

## Install Dependencies

```bash
uv sync
```

`mkdocs` and `mkdocs-material` are already included in `pyproject.toml`, so the same environment can build the documentation site.

## Run the Evaluator

Default run:

```bash
uv run python main.py
```

This uses the filtered corrected dataset and writes to:

```text
results/2wikimqa_200_samples_from_blend_filter/
```

Fast local debug run:

```bash
uv run python main.py --debug-mode --max-samples 5
```

In debug mode, the script skips API calls and returns a mock response of `yes` for each sample. This is useful for verifying prompt construction, batching flow, file output, and metric plumbing without depending on a live endpoint.

## Build the Documentation Site

Serve docs locally with live reload:

```bash
uv run mkdocs serve
```

Build static documentation:

```bash
uv run mkdocs build
```

By default, MkDocs reads `mkdocs.yml` and renders pages from `docs/`.

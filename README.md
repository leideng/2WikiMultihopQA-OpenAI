# 2WikiMultihopQA-OpenAI

Evaluate OpenAI-compatible chat models on a small `2WikiMultihopQA` slice and save per-sample QA metrics to CSV.

## Overview

`main.py` loads a JSON dataset, builds a prompt from each sample's context passages, sends async batched chat-completion requests, and computes:

- `F1`
- `Precision`
- `Recall`
- `ROUGE-L`

The repository now includes corrected dataset variants:

- `data/2wikimqa_200_samples_from_blend.json`: original 200-sample file
- `data/2wikimqa_200_samples_from_blend_fix.json`: corrected answers, including explicit overrides such as sample 1 -> `Croatia`
- `data/2wikimqa_200_samples_from_blend_filter.json`: corrected dataset with all `No answer` samples removed

By default, `main.py` evaluates the filtered dataset and writes results under `results/2wikimqa_200_samples_from_blend_filter/`.

## Requirements

- Python `>= 3.11`
- `uv`
- An OpenAI-compatible API endpoint
- Environment variables:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`

Install dependencies with:

```bash
uv sync
```

## Quick Start

Run the default evaluation:

```bash
uv run python main.py
```

Run a small local sanity check without API calls:

```bash
uv run python main.py --debug-mode --max-samples 5
```

Evaluate the corrected full dataset instead of the filtered one:

```bash
uv run python main.py \
  --eval-dataset-path data/2wikimqa_200_samples_from_blend_fix.json \
  --save-results-path results/2wikimqa_200_samples_from_blend_fix/kimi-k2.5.csv
```

Smoke-test the endpoint:

```bash
uv run python test.py
```

## Dataset Correction Utility

Use `fix_2wikimqa_no_answers.py` to regenerate the corrected datasets:

```bash
python fix_2wikimqa_no_answers.py
```

It produces:

- `data/2wikimqa_200_samples_from_blend_fix.json`
- `data/2wikimqa_200_samples_from_blend_filter.json`

The script applies both bulk `No answer` rewrites and explicit answer overrides.

## CLI Options

Key flags:

```text
--model-name
--eval-dataset-path
--save-results-path
--enable-thinking
--max-completion-tokens
--max-samples
--request-batch-size
--debug-mode
```

Use `uv run python main.py --help` for the full argparse output.

## Output Format

Each CSV contains one row per evaluated sample:

`index, question, gold, response, f1, precision, recall, rl`

A final summary row appends dataset averages in the last four columns.

## Repository Layout

- `main.py`: evaluation entry point
- `fix_2wikimqa_no_answers.py`: dataset correction script
- `test.py`, `test-qwen3-8b.py`: endpoint smoke tests
- `data/`: source and corrected JSON datasets
- `results/`: CSV outputs grouped by dataset variant

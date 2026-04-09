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

## Suggested Prompts

The repository currently recommends two prompt variants depending on which dataset you evaluate.

Use this LongBench-style short-answer prompt for:

- `data/2wikimqa_200_samples_from_blend.json`
- `data/2wikimqa_200_samples_from_blend_fix.json`

```python
prompt = (
    "Answer the question using only the provided passages. "
    "Return only the short answer phrase, with no explanation. "
    "Do not add trailing punctuation. "
    "For yes/no questions, return exactly 'yes' or 'no'. "
    "\nPassages:\n"
    f"{context}\n"
    f"\nQuestion: {question}\n"
    "Answer:"
)
```

Use this stricter prompt for:

- `data/2wikimqa_200_samples_from_blend_filter.json`

```python
prompt = (
    f"Answer the question based strictly on the provided passages. "
    f"If the answer is not present in the context, output exactly 'No answer'. "
    f"Provide only the answer itself without any surrounding punctuation like periods or commas and any other words. "
    f"Do not include any introductory or explanatory text.\n\n"
    f"Passages:\n{context}\n\n"
    f"Question: {question}\n"
    f"Answer:"
)
```

`main.py` currently keeps the first prompt active and leaves the second one as a commented alternative. See `docs/prompts.md` for the prompt guidance in the MkDocs site.

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

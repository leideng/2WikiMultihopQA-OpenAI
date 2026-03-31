# 2WikiMultihopQA-OpenAI

Evaluate an OpenAI-compatible chat model on the `2WikiMultihopQA` benchmark and save per-sample metrics (`F1`, `Precision`, `Recall`, `ROUGE-L`) to CSV.

## What this project does

`main.py` loads a JSON evaluation set, builds a prompt from each sample's passages, sends async batched requests to a model endpoint, and computes QA metrics against gold answers.

By default it evaluates:

- Dataset: `data/2wikimqa_200_samples_from_blend.json`
- Sample count: `200`
- Model name: `kimi-k2.5`
- Output file: `results/{model_name}.csv`

## Requirements

- Python `>= 3.11`
- `uv` installed
- An OpenAI-compatible API endpoint
- Environment variables:
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`

## Install

```bash
uv sync
```

## Quick start

Run with defaults:

```bash
uv run python main.py
```

Run with explicit model and output path:

```bash
uv run python main.py \
  --model-name gpt-4.1-mini \
  --save-results-path results/gpt-4.1-mini.csv
```

Run in debug mode (no API calls, returns mock responses):

```bash
uv run python main.py --debug-mode --max-samples 5
```

Run tests:

```bash
uv run python test.py
```

## CLI options

```text
--model-name                Model name for chat completions
--eval-dataset-path         Path to evaluation dataset JSON
--save-results-path         Path to output CSV
--enable-thinking           Enable model thinking mode
--max-completion-tokens     Max completion tokens per request
--max-samples               Number of samples to evaluate
--request-batch-size        Async request batch size / concurrency
--debug-mode                Skip API calls and use mock outputs
```

## Output

The CSV file contains one row per sample:

`index, question, gold, response, f1, precision, recall, rl`

At the end, one summary row is appended with average metrics in the last four columns.

## First data point walkthrough

From `data/2wikimqa_200_samples_from_blend.json`, the first sample asks:

- **Question:** `Where was the wife of Francis I Rákóczi born?`
- **Gold answer:** `Ozalj`
- **Passages:** 10 context chunks (`ctxs`)

Why the answer is `Ozalj`:

- The sample contains passages about Francis I Rákóczi and his wife (`Jelena Zrinska` / `Ilona Zrinyi`).
- `Jelena Zrinska` is a Croatian countess from Ozalj (historically connected to the Zrinski family).
- Therefore, the expected short answer is `Ozalj`.

This is a good example of multi-hop QA: the model must connect entity mentions across biography-style passages and return only the final location.

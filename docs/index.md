# 2WikiMultihopQA-OpenAI

`2WikiMultihopQA-OpenAI` evaluates OpenAI-compatible chat models on a compact `2WikiMultihopQA` slice and writes per-sample metrics to CSV.

The repository centers on a single async evaluator script, `main.py`, plus a dataset correction utility, `fix_2wikimqa_no_answers.py`, and a pair of endpoint smoke tests.

## What It Does

- Loads a JSON evaluation dataset from `data/`
- Builds a prompt from each sample's question and supporting passages
- Sends batched async chat-completion requests to an OpenAI-compatible endpoint
- Computes `F1`, `Precision`, `Recall`, and `ROUGE-L`
- Writes one CSV row per evaluated sample, followed by a final summary row

## Repository Layout

| Path | Purpose |
| --- | --- |
| `main.py` | Main evaluation entry point |
| `fix_2wikimqa_no_answers.py` | Regenerates corrected datasets |
| `test.py` | Generic endpoint smoke test |
| `test-qwen3-8b.py` | Qwen-specific smoke test |
| `data/` | Source and corrected dataset JSON files |
| `results/` | Generated benchmark CSV outputs |

## Defaults

The evaluator currently defaults to:

- Model: `kimi-k2.5`
- Dataset: `data/2wikimqa_200_samples_from_blend_filter.json`
- Max completion tokens: `20`
- Max samples: `200`
- Request batch size: `20`
- Output path template: `results/2wikimqa_200_samples_from_blend_filter/{model_name}.csv`

## Start Here

- Use [Getting Started](getting-started.md) for installation, environment variables, and the first run
- Use [Evaluation Pipeline](evaluation.md) for CLI flags and runtime behavior
- Use [Datasets](datasets.md) for the corrected dataset workflow
- Use [Results](results.md) to understand CSV outputs and directory conventions
- Use [Smoke Tests](smoke-tests.md) to validate endpoint connectivity before a full run

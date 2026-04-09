# Evaluation Pipeline

## Runtime Flow

`main.py` follows this sequence:

1. Parse CLI arguments.
2. Resolve the output CSV path.
3. Read `OPENAI_API_KEY` and `OPENAI_BASE_URL` unless `--debug-mode` is enabled.
4. Load the evaluation dataset JSON file.
5. Build one prompt per sample from the question and its `ctxs` passages.
6. Send batched async chat-completion requests through `AsyncOpenAI`.
7. Compute `F1`, `Precision`, `Recall`, and `ROUGE-L`.
8. Append per-sample rows and a final average row to the output CSV.

## Prompt Behavior

For each sample, the evaluator concatenates all context passages and uses a short-answer instruction:

```text
Answer the question using only the provided passages.
Return only the short answer phrase, with no explanation.
Do not add trailing punctuation.
For yes/no questions, return exactly 'yes' or 'no'.
```

This keeps outputs short and aligned with extractive QA-style scoring.

## Main CLI Flags

| Flag | Meaning | Default |
| --- | --- | --- |
| `--model-name` | Chat model name sent to the endpoint | `kimi-k2.5` |
| `--eval-dataset-path` | Input dataset JSON file | `data/2wikimqa_200_samples_from_blend_filter.json` |
| `--save-results-path` | Output CSV path | Derived from model name |
| `--enable-thinking` | Enables provider-specific reasoning mode when supported | Disabled |
| `--max-completion-tokens` | Max completion tokens per request | `20` |
| `--max-samples` | Maximum number of dataset rows to evaluate | `200` |
| `--request-batch-size` | Async concurrency and batch size | `20` |
| `--debug-mode` | Skip API calls and use mock responses | Disabled |

## Common Commands

Run the default filtered benchmark:

```bash
uv run python main.py
```

Run only five samples locally:

```bash
uv run python main.py --debug-mode --max-samples 5
```

Use a different model name:

```bash
uv run python main.py --model-name gpt-5.4
```

Override the dataset and output location:

```bash
uv run python main.py \
  --eval-dataset-path data/2wikimqa_200_samples_from_blend_fix.json \
  --save-results-path results/2wikimqa_200_samples_from_blend_fix/kimi-k2.5.csv
```

## Notes on Provider Compatibility

The script uses the OpenAI chat-completions interface via the `openai` Python SDK. When `--enable-thinking` is not set, it adds:

```python
extra_body = {"reasoning_effort": "none"}
```

This matches the repository's current target behavior for GPT- and Claude-style OpenAI-compatible backends. If a provider expects a different extension field, update `main.py` accordingly.

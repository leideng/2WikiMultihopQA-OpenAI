# Results

## Output Convention

The evaluator writes CSV files under `results/`. The default save path template is:

```text
results/2wikimqa_200_samples_from_blend_filter/{model_name}.csv
```

This keeps outputs grouped by dataset variant, which is useful when the same model is evaluated on both fixed and filtered datasets.

## CSV Schema

Each result file begins with this header:

```text
index,question,gold,response,f1,precision,recall,rl
```

Each subsequent row represents one evaluated sample. The final row leaves the first four columns blank and stores dataset averages in the metric columns.

## Example Interpretation

| Column | Meaning |
| --- | --- |
| `index` | One-based sample index within the selected dataset slice |
| `question` | Normalized question text |
| `gold` | Gold answer string used for scoring |
| `response` | Model output |
| `f1` | Token-overlap F1 score after normalization |
| `precision` | Token-overlap precision |
| `recall` | Token-overlap recall |
| `rl` | `ROUGE-L` F-measure |

## Current Results Layout

The repository already contains several generated artifacts, including:

- `results/2wikimqa_200_samples_from_blend/`
- `results/2wikimqa_200_samples_from_blend_fix/`
- `results/2wikimqa_200_samples_from_blend_filter/`

Treat files under `results/` as generated outputs. Keep them only when they represent intentional benchmark results you want to preserve.

## Reproducibility Tips

- Record the dataset variant alongside the model name.
- Keep the exact CLI command used for a run.
- If you change prompts or scoring logic, write results to a new file instead of overwriting older benchmark baselines blindly.

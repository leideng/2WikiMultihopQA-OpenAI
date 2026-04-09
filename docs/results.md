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

## Full Published Result Pages

This documentation site also includes verbatim copies of the key benchmark CSVs so readers can inspect every row directly in the docs:

- [Original 200 / doubao-seed-2.0-pro](results-original-doubao.md)
- [Fixed 200 / doubao-seed-2.0-pro](results-fixed-doubao.md)
- [Filtered 102 / doubao-seed-2.0-pro](results-filtered-doubao.md)
- [Filtered 102 / gpt-5.4](results-filtered-gpt-5.4.md)
- [Filtered 102 / claude-opus-4.6](results-filtered-claude-opus-4.6.md)

Each page reproduces the corresponding CSV content in full.

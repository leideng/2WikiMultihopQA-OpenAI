# Datasets

## Available Dataset Files

The repository contains three benchmark variants under `data/`:

| File | Description |
| --- | --- |
| `data/2wikimqa_200_samples_from_blend.json` | Original 200-sample file |
| `data/2wikimqa_200_samples_from_blend_fix.json` | Corrected dataset with answer rewrites and explicit overrides |
| `data/2wikimqa_200_samples_from_blend_filter.json` | Corrected dataset with all `No answer` samples removed |

The default evaluator path points to the filtered corrected dataset.

## Correction Utility

Use `fix_2wikimqa_no_answers.py` to regenerate the corrected files:

```bash
python fix_2wikimqa_no_answers.py
```

It writes:

- `data/2wikimqa_200_samples_from_blend_fix.json`
- `data/2wikimqa_200_samples_from_blend_filter.json`

## What the Script Changes

The correction script applies two categories of edits:

- Bulk rewrites for indices listed in `NO_ANSWER_INDICES`
- Explicit answer replacements listed in `ANSWER_OVERRIDES`

After writing the fixed dataset, it creates a filtered dataset by removing any samples whose answer becomes `["No answer"]`.

## Optional CLI Arguments

The correction script also supports custom paths:

```bash
python fix_2wikimqa_no_answers.py \
  --input-path data/2wikimqa_200_samples_from_blend.json \
  --output-path data/2wikimqa_200_samples_from_blend_fix.json \
  --filtered-output-path data/2wikimqa_200_samples_from_blend_filter.json
```

## Choosing a Dataset Variant

Use the filtered dataset when you want the repository's current default benchmark behavior.

Use the fixed full dataset when you want to preserve all 200 original sample slots while still applying corrections.

Use the original dataset only if you intentionally need the untouched source file for comparison or reproducibility work.

# CacheBlend Issue Notes

This page documents the rationale behind the issue submitted to the CacheBlend repository about the published `2WikiMultihopQA` sample file and the evaluation workflow around it.

## Background

The original CacheBlend repository publishes a 200-sample benchmark file at `inputs/wikimqa_s.json`. This repository copied that file into:

```text
data/2wikimqa_200_samples_from_blend.json
```

During reproduction and benchmarking work, the dataset was audited against the supplied context passages. That audit found two recurring problems:

- some published gold answers are incorrect relative to the provided context
- some questions are not answerable from the provided context at all

Because this benchmark is often used as a sanity check for long-context KV-cache reuse methods, these label issues materially affect reported accuracy.

## Problem Categories

### Incorrect Gold Answers

Some rows have a published answer that is not what the provided context supports.

Example: sample 1

Question:

```text
Where was the wife of Francis I Rakoczi born?
```

Published gold:

```text
Ozalj
```

However, the context supports `Croatia`, not `Ozalj`. The fixed dataset therefore replaces sample 1 with:

```text
Croatia
```

### Unanswerable Samples

Some rows ask about entities or relations that are not actually present in the supplied context blocks.

Example: sample 11

Question:

```text
Which film has the director who was born earlier, The Secret Invasion or The House Of The Seven Hawks?
```

Published gold:

```text
The House Of The Seven Hawks
```

But the provided context does not support this answer. In particular, the second film is not present in the supplied context chunks, so the sample is not answerable from the benchmark input alone.

The correction policy used in this repository marks this row as:

```text
No answer
```

## Correction Policy

The correction policy is intentionally simple and auditable:

- mark unsupported rows as `No answer`
- replace clearly incorrect gold answers with the answer supported by the provided context

The implementation lives in `fix_2wikimqa_no_answers.py`.

### Unanswerable Rows

The current bulk list is:

```python
NO_ANSWER_INDICES = [
    4, 9, 11, 15, 16, 18, 20, 21, 22, 29, 30, 34, 37, 39, 41, 44, 45, 46, 47,
    50, 51, 53, 55, 56, 58, 60, 64, 65, 66, 67, 68, 70, 74, 75, 78, 79, 81,
    83, 84, 85, 87, 88, 95, 99, 101, 102, 104, 106, 107, 108, 109, 110, 112,
    114, 115, 116, 120, 121, 122, 123, 126, 129, 130, 131, 132, 134, 137, 138,
    139, 141, 142, 147, 149, 152, 153, 156, 160, 163, 168, 169, 173, 177, 178,
    179, 180, 181, 182, 183, 184, 186, 187, 188, 194, 196, 197, 198, 199, 200,
]
```

### Explicit Gold Overrides

The current explicit replacement list is:

```python
ANSWER_OVERRIDES = {
    1: [["Croatia"]],
    3: [["Odeon - Theatre de l'Europe"]],
    6: [["Edward Watson, 2nd Baron Rockingham"]],
    12: [["Margaret of Flanders"]],
    13: [["John I, count of soissons"]],
    28: [["No"]],
    32: [["Jean Paul Getty"]],
    40: [["Istanbul"]],
    48: [["Faustina the Elder"]],
    69: [["La Belle Américaine"]],
    71: [["Iranian hospital Dubai"], ["Dubai"]],
    72: [["France"]],
    77: [["Egypt"]],
    89: [["Hawaii"]],
    94: [["1839"]],
    96: [["francoise hardy"]],
    98: [["Washington, D. C."]],
    100: [["fernan blazquez de caceres"]],
    103: [["Denmark"]],
    105: [["Harby"]],
    117: [["Methala"]],
    125: [["Waiting For The Clouds"]],
    128: [["University of Wisconsin-Madison"]],
    143: [["Crenshaw"]],
    145: [["Adolf II of Berg-Hovel"]],
    150: [["Mongkut"]],
    154: [["orange county, virginia"]],
    155: [["Mangalia, Romania"]],
    157: [["jacques de savoie"]],
    158: [["Geza, Grand Prince of the Hungarians"]],
    159: [["Queen Yi Jiang"]],
    161: [["Ivy Duke and Dorothy Batley"]],
    166: [["Oxford University"]],
    171: [["Best Cutting Edge Film"]],
    172: [["German"]],
    174: [["Inverkeithing"]],
    175: [["1234"]],
    176: [["1666"]],
    190: [["Vienna"]],
    193: [["English"]],
}
```

## Corrected Dataset Variants

This repository exposes two corrected derivatives of the original 200-sample file:

- `data/2wikimqa_200_samples_from_blend_fix.json`
- `data/2wikimqa_200_samples_from_blend_filter.json`

The first preserves the 200-row benchmark while applying corrections. The second removes all rows whose corrected answer is `No answer`, producing a cleaner answerable-only evaluation slice.

## Metric Impact

Using the evaluation code in this repository, the reported summary metrics change substantially once the dataset is corrected.

| Setting | F1 | Precision | Recall | ROUGE-L |
| --- | ---: | ---: | ---: | ---: |
| Original 200 / `doubao-seed-2.0-pro` | 0.4403 | 0.4270 | 0.5132 | 0.4518 |
| Fixed 200 / `doubao-seed-2.0-pro` | 0.7870 | 0.7802 | 0.8087 | 0.7877 |
| Filtered 102 / `doubao-seed-2.0-pro` | 0.8327 | 0.8166 | 0.8901 | 0.8387 |
| Filtered 102 / `gpt-5.4` | 0.7899 | 0.7846 | 0.8288 | 0.7956 |
| Filtered 102 / `claude-opus-4.6` | 0.7500 | 0.7500 | 0.7950 | 0.7672 |

These deltas strongly suggest that the original gold labels suppress measured performance for capable models.

## Why This Matters

If a benchmark contains unsupported or incorrect labels, the resulting score mixes model quality with annotation noise. For CacheBlend-style systems, that is especially problematic because:

- `2WikiMultihopQA` is often used as a compact multi-hop reasoning validation task
- the benchmark is reused across reproduction efforts and system comparisons
- poor labels can make strong models look much worse than they are

This means benchmark conclusions can become unstable or misleading even when the serving stack and inference logic are correct.

## Evaluation Workflow Suggestion

The issue also argues for a cleaner benchmarking interface.

Instead of coupling benchmark execution to an offline, project-specific inference stack, accuracy evaluation should accept a standard OpenAI-compatible interface:

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`

That design makes it easier to benchmark:

- hosted commercial APIs
- self-hosted online serving systems such as vLLM
- different backends behind one shared evaluation script

This repository follows that approach in `main.py`, which uses the `openai` Python SDK and an OpenAI-compatible `base_url` rather than hard-wiring the evaluator to one inference backend.

## Practical Takeaway

If you are reproducing CacheBlend-style results, use one of the corrected datasets in this repository instead of the original copied sample file unless you explicitly need the original for comparison.

If you are reporting results, document which dataset variant you used:

- original 200-sample file
- fixed 200-sample file
- filtered 102-sample file

Without that distinction, cross-run comparisons are easy to misread.

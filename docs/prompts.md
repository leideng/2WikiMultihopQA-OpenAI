# Suggested Prompts

This page documents the two prompt variants currently recommended for this repository.

The distinction matters because the original CacheBlend-derived 200-sample file and the fixed 200-sample file still include rows that may be unsupported or intentionally labeled as `No answer`, while the filtered dataset removes all such rows.

## Prompt Selection

Use the first prompt for:

- `data/2wikimqa_200_samples_from_blend.json`
- `data/2wikimqa_200_samples_from_blend_fix.json`

Use the second prompt for:

- `data/2wikimqa_200_samples_from_blend_filter.json`

## Prompt For Original And Fixed Datasets

This is the current active prompt in `main.py`. It follows the LongBench-style short-answer format and does not explicitly force `No answer`.

```text
Answer the question using only the provided passages. Return only the short answer phrase, with no explanation. Do not add trailing punctuation. For yes/no questions, return exactly 'yes' or 'no'.
Passages:
{context}

Question: {question}
Answer:
```

Python form:

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

## Prompt For Filtered Dataset

This is the suggested stricter prompt for the filtered dataset. It tells the model to stay within the provided context and emit `No answer` if support is absent.

```text
Answer the question based strictly on the provided passages. If the answer is not present in the context, output exactly 'No answer'. Provide only the answer itself without any surrounding punctuation like periods or commas and any other words. Do not include any introductory or explanatory text.

Passages:
{context}

Question: {question}
Answer:
```

Python form:

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

## Why The Recommendation Differs By Dataset

For the original and fixed 200-row datasets, the benchmark still contains rows where the model may be pushed into unsupported comparisons or partially mismatched annotations. A shorter extraction-style prompt is the safer baseline because it does not overfit to explicit abstention behavior.

For the filtered dataset, all `No answer` rows have already been removed. The stricter prompt is still useful because it reduces extra narration and keeps the model anchored to the provided passages.

## Current Code State

`main.py` currently leaves the first prompt active and keeps the second prompt as a commented recommended alternative. If you want to benchmark the filtered dataset with the stricter prompt, replace the active prompt block with the second version before running evaluation.

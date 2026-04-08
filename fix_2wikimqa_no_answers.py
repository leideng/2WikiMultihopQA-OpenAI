import argparse
import json
from pathlib import Path


NO_ANSWER_INDICES = [
    4, 9, 11, 15, 16, 18, 20, 21, 22, 29, 30, 34, 37, 39, 41, 44, 45, 46, 47,
    50, 51, 53, 55, 56, 58, 60, 64, 65, 66, 67, 68, 70, 74, 75, 78, 79, 81,
    83, 84, 85, 87, 88, 95, 99, 101, 102, 104, 106, 107, 108, 109, 110, 112,
    114, 115, 116, 120, 121, 122, 123, 126, 129, 130, 131, 132, 134, 137, 138,
    139, 141, 142, 147, 149, 152, 153, 156, 160, 163, 168, 169, 173, 177, 178,
    179, 180, 181, 182, 183, 184, 186, 187, 188, 194, 196, 197, 198, 199, 200,
]

DEFAULT_INPUT_PATH = "data/2wikimqa_200_samples_from_blend.json"
DEFAULT_OUTPUT_PATH = "data/2wikimqa_200_samples_from_blend_fix.json"
NO_ANSWER_VALUE = [["No answer"]]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Rewrite selected 2WikiMultihopQA samples to use 'No answer'."
    )
    parser.add_argument(
        "--input-path",
        default=DEFAULT_INPUT_PATH,
        help=f"Source dataset path (default: {DEFAULT_INPUT_PATH}).",
    )
    parser.add_argument(
        "--output-path",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Fixed dataset path (default: {DEFAULT_OUTPUT_PATH}).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    if len(data) < max(NO_ANSWER_INDICES):
        raise ValueError(
            f"Dataset has {len(data)} samples, but index {max(NO_ANSWER_INDICES)} was requested."
        )

    for sample_index in NO_ANSWER_INDICES:
        data[sample_index - 1]["answers"] = NO_ANSWER_VALUE

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )

    print(
        f"Wrote {output_path} with {len(NO_ANSWER_INDICES)} samples set to {NO_ANSWER_VALUE[0][0]!r}."
    )


if __name__ == "__main__":
    main()

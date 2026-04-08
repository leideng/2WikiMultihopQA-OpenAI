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
DEFAULT_FILTERED_OUTPUT_PATH = "data/2wikimqa_200_samples_from_blend_filter.json"
NO_ANSWER_VALUE = [["No answer"]]

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
    69: [["La Belle Américaine"]],  # Added missing quotes
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
    158: [["Géza, Grand Prince of the Hungarians"]],
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply answer corrections to the 2WikiMultihopQA sample set."
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
    parser.add_argument(
        "--filtered-output-path",
        default=DEFAULT_FILTERED_OUTPUT_PATH,
        help=(
            "Filtered dataset path with all 'No answer' samples removed "
            f"(default: {DEFAULT_FILTERED_OUTPUT_PATH})."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    filtered_output_path = Path(args.filtered_output_path)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    if len(data) < max(NO_ANSWER_INDICES):
        raise ValueError(
            f"Dataset has {len(data)} samples, but index {max(NO_ANSWER_INDICES)} was requested."
        )

    for sample_index in NO_ANSWER_INDICES:
        data[sample_index - 1]["answers"] = NO_ANSWER_VALUE

    for sample_index, replacement_answer in ANSWER_OVERRIDES.items():
        data[sample_index - 1]["answers"] = replacement_answer

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )

    filtered_data = [
        sample for sample in data if sample.get("answers") != NO_ANSWER_VALUE
    ]
    filtered_output_path.write_text(
        json.dumps(filtered_data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )

    print(
        "Wrote "
        f"{output_path} with {len(NO_ANSWER_INDICES)} 'No answer' rewrites "
        f"and {len(ANSWER_OVERRIDES)} explicit answer overrides."
    )
    print(
        f"Wrote {filtered_output_path} with {len(filtered_data)} samples after filtering."
    )


if __name__ == "__main__":
    main()

"""Convert original dataset format to new format.

Usage:
    python convert_original_to_new_format.py <input_file> <output_prefix>

Example:
    python convert_original_to_new_format.py dataset_sampled/train_subset.json dataset_sampled/train_original
"""
import sys
import json
from tqdm import tqdm

def convert_format(original_data):
    # Check the data format for unhandled cases.
    unhandled = [
        "user_prompt",
        "text_document",
        "instruct_sep_tags",
        "data_sep_tags"
    ]
    for item in unhandled:
        if item in original_data[0]:
            if original_data[0][item] != "none":
                print(f"Data contains '{item}', which is not handled in this conversion script.")
                sys.exit(1)

    # Do the conversion: this splits each example into a clean and a poisoned example.
    clean_data = []
    poisoned_data = []

    for dataset_item in tqdm(original_data):
        clean_data.append({
            "sep_prompt": dataset_item["sep_prompt"],
            "user_prompt": dataset_item["primary_task_prompt"],
            "text_document": dataset_item["orig_text"]
        })
        poisoned_data.append({
            "sep_prompt": dataset_item["sep_prompt"],
            "user_prompt": dataset_item["primary_task_prompt"],
            "text_document": dataset_item["final_text_paragraph"]
        })

    return clean_data, poisoned_data


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_original_to_new_format.py <input_file> <output_prefix>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_prefix = sys.argv[2]

    print(f"Converting data from {input_file} and saving to {output_prefix}_clean.json and {output_prefix}_poisoned.json")
    with open(input_file, "r") as f:
        original_data = json.load(f)

    clean_data, poisoned_data = convert_format(original_data)

    print("Saving converted data.")
    with open(f"{output_prefix}_clean.json", "w") as f:
        json.dump(clean_data, f)

    with open(f"{output_prefix}_poisoned.json", "w") as f:
        json.dump(poisoned_data, f)
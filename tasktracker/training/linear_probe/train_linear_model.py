"""Trains a logistic regression probe on the given activations data.
"""
import os
import json
import pickle
import torch
import numpy as np
from tqdm import tqdm
from pathlib import Path
from sklearn.linear_model import LogisticRegression


# MODEL = "gpt_oss_20b_harmony"
MODEL = "phi3"
ACTIVATIONS_DIR = Path(__file__).parent.parent.parent.parent / f"disk3/activations/{MODEL}/train"
OUTPUT_DIR = str(
    Path(__file__).parent.parent.parent.parent / "trained_linear_probes" / MODEL
)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Which layers would be used for training probes
LAYERS_PER_MODEL = {
    "llama3_70b": [0, 7, 15, 23, 31, 39, 47, 55, 63, 71, 79],
    "phi3": [0, 7, 15, 23, 31],
    "mixtral": [0, 7, 15, 23, 31],
    "mistral": [0, 7, 15, 23, 31],
    "llama3_8b": [0, 7, 15, 23, 31],
    "mistral_no_priming": [0, 7, 15, 23, 31],
    "gpt_oss_20b": [0, 7, 15, 23],
    "gpt_oss_20b_primed": [0, 7, 15, 23],
    "gpt_oss_20b_harmony": [0, 7, 15, 23],
    "gpt_oss_20b_harmony_primed": [0, 7, 15, 23],
}
LAYERS = LAYERS_PER_MODEL[MODEL]


# Configuration settings
config = {
    "activations": str(ACTIVATIONS_DIR),
    "exp_name": "logistic_regression_" + MODEL,
}

def load_activation_deltas(files, num_layers):
    """Loads the activations and computes the deltas in a single step.
    This reduces the memory overhead.
    """
    deltas = []
    for fname in tqdm(files):
        curr_file = torch.load(os.path.join(ACTIVATIONS_DIR, fname))

        if isinstance(num_layers, int):
            activation = curr_file[:, :, -num_layers :, :]

        elif isinstance(num_layers, tuple):
            activation = curr_file[
                :, :, num_layers[0] : num_layers[1] + 1, :
            ]
        activations_primary = activation[0, :, :, :]
        activations_primary_with_text = activation[1, :, :, :]
        # Shape is [batch, 1, dim]
        delta = (activations_primary_with_text - activations_primary)
        # Flatten, but keep batch dimension.
        delta = delta.flatten(start_dim=1)
        deltas.append(delta.float().numpy())

    # Stack the batches.
    deltas = np.vstack(deltas)

    return deltas

def train_model(files_clean, files_poisoned, num_layers):
    print(f"Loading activations and computing the deltas.")
    clean_deltas = load_activation_deltas(files_clean, num_layers)
    poisoned_deltas = load_activation_deltas(files_poisoned, num_layers)

    print(f"Training the logistic regression model.")
    X = np.vstack([clean_deltas, poisoned_deltas])
    y = [0] * len(clean_deltas) + [1] * len(poisoned_deltas)

    model = LogisticRegression()
    model.fit(X, y)

    return model, X, y


if __name__ == "__main__":
    files_clean = []
    files_poisoned = []
    for fname in ACTIVATIONS_DIR.iterdir():
        if "clean" in fname.name:
            files_clean.append(str(fname))
        elif "poisoned" in fname.name:
            files_poisoned.append(str(fname))
    print(f"Found {len(files_clean)} clean files and {len(files_poisoned)} poisoned files.")

    # Option to subsample for quick testing.
    N = -1
    files_clean = files_clean[:N]
    files_poisoned = files_poisoned[:N]
    print(f"Using {len(files_clean)} clean files and {len(files_poisoned)} poisoned files.")

    for n_layer in LAYERS:
        print(f"[*] Training model for the {n_layer}-th activation layer.")
        os.makedirs(os.path.join(OUTPUT_DIR, str(n_layer)), exist_ok=True)
        layer_output_dir = os.path.join(OUTPUT_DIR, str(n_layer))

        # Store config.
        _config = config.copy()
        _config["num_layers"] = n_layer
        _config["exp_name"] = f"{config['exp_name']}_{n_layer}"
        print(_config["exp_name"])
        with open(os.path.join(layer_output_dir, "config.json"), "w") as f:
            json.dump(_config, f)

        # Train model.
        model, X, y = train_model(files_clean, files_poisoned, num_layers=(n_layer, n_layer))
        out_fname = os.path.join(layer_output_dir, "model.pickle")
        pickle.dump(model, open(out_fname, "wb"))
        print(
            f"""Model saved at {os.path.abspath(out_fname)}"""
        )

        # Evaluate.
        print("Evaluating on training set.")
        accuracy = model.score(X, y)
        print(accuracy)
        print("\n" * 4)

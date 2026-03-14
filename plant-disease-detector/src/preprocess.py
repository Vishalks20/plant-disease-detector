"""
Data Preprocessing Pipeline
============================
Splits raw PlantVillage dataset into train/val/test sets and
creates augmented TensorFlow data pipelines.

Usage:
    python src/preprocess.py --data_dir data/raw/PlantVillage
"""

import os
import json
import shutil
import argparse
import numpy as np
from pathlib import Path
from tqdm import tqdm

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from config import Config

# ────────────────────────────────────────────────────────────────────────────


def create_train_val_test_split(
    source_dir: Path,
    output_dir: Path,
    val_split: float = 0.1,
    test_split: float = 0.1,
    seed: int = 42,
):
    """
    Split raw PlantVillage directory into train/val/test sub-directories.

    Expected source structure:
        source_dir/
            ClassName_A/image1.jpg ...
            ClassName_B/image1.jpg ...
    """
    np.random.seed(seed)
    class_dirs = sorted([d for d in source_dir.iterdir() if d.is_dir()])
    print(f"Found {len(class_dirs)} classes in {source_dir}")

    splits = ["train", "val", "test"]
    for split in splits:
        (output_dir / split).mkdir(parents=True, exist_ok=True)

    class_indices = {}

    for idx, class_dir in enumerate(tqdm(class_dirs, desc="Splitting classes")):
        class_name = class_dir.name
        class_indices[class_name] = idx
        images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.JPG")) + \
                 list(class_dir.glob("*.png")) + list(class_dir.glob("*.jpeg"))
        np.random.shuffle(images)

        n = len(images)
        n_test = int(n * test_split)
        n_val  = int(n * val_split)

        split_map = {
            "test":  images[:n_test],
            "val":   images[n_test: n_test + n_val],
            "train": images[n_test + n_val:],
        }

        for split, split_images in split_map.items():
            dest = output_dir / split / class_name
            dest.mkdir(parents=True, exist_ok=True)
            for img_path in split_images:
                shutil.copy2(img_path, dest / img_path.name)

    # Save class_indices
    indices_path = Config.MODELS_DIR / "class_indices.json"
    Config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    with open(indices_path, "w") as f:
        json.dump(class_indices, f, indent=2)
    print(f"Class indices saved to {indices_path}")
    print(f"Split complete → {output_dir}")
    return class_indices


def build_data_generators(processed_dir: Path, batch_size: int = 32, img_size=(224, 224)):
    """
    Build Keras ImageDataGenerators for train / val / test sets.
    Returns (train_gen, val_gen, test_gen, class_indices)
    """
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=30,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=False,
        brightness_range=[0.8, 1.2],
        fill_mode="nearest",
    )

    eval_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        processed_dir / "train",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=True,
    )

    val_gen = eval_datagen.flow_from_directory(
        processed_dir / "val",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False,
    )

    test_gen = eval_datagen.flow_from_directory(
        processed_dir / "test",
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        shuffle=False,
    )

    return train_gen, val_gen, test_gen, train_gen.class_indices


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Preprocess PlantVillage dataset")
    parser.add_argument("--data_dir", type=str, default=str(Config.RAW_DATA_DIR))
    parser.add_argument("--output_dir", type=str, default=str(Config.PROCESSED_DIR))
    parser.add_argument("--val_split", type=float, default=Config.VALIDATION_SPLIT)
    parser.add_argument("--test_split", type=float, default=Config.TEST_SPLIT)
    args = parser.parse_args()

    source = Path(args.data_dir)
    output = Path(args.output_dir)

    if not source.exists():
        print(f"ERROR: Source directory not found: {source}")
        print("Please download the PlantVillage dataset first.")
        print("  kaggle datasets download -d emmarex/plantdisease")
        return

    create_train_val_test_split(source, output, args.val_split, args.test_split)


if __name__ == "__main__":
    main()

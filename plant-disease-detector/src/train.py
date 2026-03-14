"""
Model Training Script
======================
Trains an EfficientNetB3-based CNN for plant disease classification.

Usage:
    python src/train.py
    python src/train.py --epochs 30 --batch_size 32 --data_dir data/processed
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
)

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config
from src.preprocess import build_data_generators


# ─── Model Definition ────────────────────────────────────────────────────────

def build_model(num_classes: int, img_size=(224, 224), learning_rate=0.001) -> keras.Model:
    """Build EfficientNetB3-based transfer learning model."""

    base_model = EfficientNetB3(
        include_top=False,
        weights="imagenet",
        input_shape=(*img_size, 3),
    )

    # Phase 1: Freeze base model
    base_model.trainable = False

    inputs = keras.Input(shape=(*img_size, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs, name="PlantDiseaseNet")

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy", keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")],
    )
    return model, base_model


def unfreeze_top_layers(model, base_model, num_layers=30, learning_rate=1e-5):
    """Phase 2: Unfreeze top N layers for fine-tuning."""
    base_model.trainable = True
    for layer in base_model.layers[:-num_layers]:
        layer.trainable = False

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy", keras.metrics.TopKCategoricalAccuracy(k=5, name="top5_acc")],
    )
    print(f"Fine-tuning: unfroze top {num_layers} layers of base model.")
    return model


# ─── Callbacks ────────────────────────────────────────────────────────────────

def get_callbacks(model_save_path: Path, log_dir: Path) -> list:
    log_dir.mkdir(parents=True, exist_ok=True)
    return [
        ModelCheckpoint(
            filepath=str(model_save_path),
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1,
        ),
        EarlyStopping(
            monitor="val_accuracy",
            patience=7,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1,
        ),
        TensorBoard(log_dir=str(log_dir), histogram_freq=1),
    ]


# ─── Training ────────────────────────────────────────────────────────────────

def train(args):
    print("=" * 60)
    print("  Plant Disease Detection — Training Pipeline")
    print("=" * 60)

    # Check GPU
    gpus = tf.config.list_physical_devices("GPU")
    print(f"GPUs available: {len(gpus)}")
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

    processed_dir = Path(args.data_dir)
    if not processed_dir.exists():
        print(f"ERROR: Processed data directory not found: {processed_dir}")
        print("Run: python src/preprocess.py --data_dir <raw_data_dir>")
        return

    # Data generators
    print("\nLoading data generators...")
    train_gen, val_gen, test_gen, class_indices = build_data_generators(
        processed_dir, batch_size=args.batch_size
    )
    num_classes = len(class_indices)
    print(f"Classes: {num_classes} | Train: {train_gen.samples} | Val: {val_gen.samples}")

    # Save class indices
    Config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    with open(Config.CLASS_INDICES, "w") as f:
        json.dump(class_indices, f, indent=2)

    # Build model
    print("\nBuilding model (EfficientNetB3)...")
    model, base_model = build_model(num_classes, learning_rate=args.lr)
    model.summary()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path("logs") / timestamp
    callbacks = get_callbacks(Config.MODEL_PATH, log_dir)

    # ── Phase 1: Train classifier head ────────────────────────────────────
    print(f"\n{'─'*40}")
    print("  Phase 1: Training classifier head")
    print(f"{'─'*40}")
    history1 = model.fit(
        train_gen,
        epochs=min(args.epochs, 10),
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1,
    )

    # ── Phase 2: Fine-tune ────────────────────────────────────────────────
    if args.epochs > 10:
        print(f"\n{'─'*40}")
        print("  Phase 2: Fine-tuning top layers")
        print(f"{'─'*40}")
        model = unfreeze_top_layers(model, base_model, num_layers=30, learning_rate=1e-5)
        history2 = model.fit(
            train_gen,
            epochs=args.epochs - 10,
            validation_data=val_gen,
            callbacks=callbacks,
            verbose=1,
        )

    # ── Evaluation ────────────────────────────────────────────────────────
    print(f"\n{'─'*40}")
    print("  Final Evaluation on Test Set")
    print(f"{'─'*40}")
    loss, acc, top5 = model.evaluate(test_gen, verbose=1)
    print(f"\nTest Loss    : {loss:.4f}")
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print(f"Top-5 Accuracy: {top5 * 100:.2f}%")

    model.save(str(Config.MODEL_PATH))
    print(f"\nModel saved to: {Config.MODEL_PATH}")
    print("Training complete!")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="Train plant disease detection model")
    parser.add_argument("--data_dir",   type=str,   default=str(Config.PROCESSED_DIR))
    parser.add_argument("--epochs",     type=int,   default=Config.EPOCHS)
    parser.add_argument("--batch_size", type=int,   default=Config.BATCH_SIZE)
    parser.add_argument("--lr",         type=float, default=Config.LEARNING_RATE)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(args)

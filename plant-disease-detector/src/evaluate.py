"""
Model Evaluation Script
========================
Generates confusion matrix, classification report, and sample predictions.

Usage:
    python src/evaluate.py --data_dir data/processed
"""

import sys
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config
from src.preprocess import build_data_generators
from src.utils.helpers import load_class_indices


def evaluate_model(args):
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Model not found at {model_path}")
        return

    print("Loading model...")
    model = tf.keras.models.load_model(str(model_path))

    print("Loading data...")
    processed_dir = Path(args.data_dir)
    _, _, test_gen, class_indices = build_data_generators(
        processed_dir, batch_size=args.batch_size
    )

    idx_to_class = {v: k for k, v in class_indices.items()}

    # Predictions
    print("Running predictions on test set...")
    test_gen.reset()
    y_pred_probs = model.predict(test_gen, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = test_gen.classes

    # Metrics
    accuracy = np.mean(y_pred == y_true)
    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")

    class_names = [idx_to_class[i] for i in range(len(class_indices))]
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names, zero_division=0))

    # Confusion Matrix Plot
    if args.save_plots:
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)

        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(20, 18))
        sns.heatmap(cm, annot=False, fmt="d", cmap="Blues",
                    xticklabels=class_names, yticklabels=class_names)
        plt.title("Confusion Matrix — Plant Disease Classifier", fontsize=16)
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.xticks(rotation=90, fontsize=7)
        plt.yticks(rotation=0, fontsize=7)
        plt.tight_layout()
        plot_path = output_dir / "confusion_matrix.png"
        plt.savefig(plot_path, dpi=150)
        print(f"Confusion matrix saved to {plot_path}")
        plt.close()

        # Per-class accuracy bar chart
        per_class_acc = cm.diagonal() / cm.sum(axis=1)
        plt.figure(figsize=(16, 6))
        colors = ["#2ecc71" if a >= 0.9 else "#e74c3c" for a in per_class_acc]
        plt.bar(range(len(class_names)), per_class_acc, color=colors)
        plt.xticks(range(len(class_names)), class_names, rotation=90, fontsize=7)
        plt.ylabel("Accuracy")
        plt.title("Per-Class Accuracy")
        plt.axhline(y=0.9, color="gray", linestyle="--", label="90% threshold")
        plt.tight_layout()
        bar_path = output_dir / "per_class_accuracy.png"
        plt.savefig(bar_path, dpi=150)
        print(f"Per-class accuracy chart saved to {bar_path}")
        plt.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate plant disease model")
    parser.add_argument("--data_dir",   type=str, default=str(Config.PROCESSED_DIR))
    parser.add_argument("--model",      type=str, default=str(Config.MODEL_PATH))
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--save_plots", action="store_true", default=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    evaluate_model(args)

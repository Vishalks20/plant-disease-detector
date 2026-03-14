"""General utility functions for image processing and model helpers."""

import os
import json
import numpy as np
from pathlib import Path
from PIL import Image, ImageOps
import tensorflow as tf


def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """Load an image from path and preprocess for model input."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size, Image.LANCZOS)
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dim
    return img_array


def preprocess_pil_image(pil_image, target_size=(224, 224)):
    """Preprocess a PIL image object for model input."""
    img = pil_image.convert("RGB").resize(target_size, Image.LANCZOS)
    img_array = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(img_array, axis=0)


def load_class_indices(json_path):
    """Load class index mapping from JSON file."""
    with open(json_path, "r") as f:
        class_indices = json.load(f)
    # Invert: {index -> class_name}
    return {int(v): k for k, v in class_indices.items()}


def get_top_k_predictions(predictions, idx_to_class, k=5):
    """Return top-k predictions as list of dicts."""
    pred_array = predictions[0]
    top_k_indices = np.argsort(pred_array)[::-1][:k]
    results = []
    for idx in top_k_indices:
        results.append({
            "class": idx_to_class.get(idx, f"class_{idx}"),
            "confidence": float(pred_array[idx]),
        })
    return results


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed."""
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_uploaded_file(file_obj, upload_folder, filename):
    """Save uploaded file to folder safely."""
    os.makedirs(upload_folder, exist_ok=True)
    filepath = Path(upload_folder) / filename
    file_obj.save(str(filepath))
    return str(filepath)


def is_plant_image(img_array, threshold=0.3):
    """
    Heuristic check: does the image contain significant green tones?
    Returns True if image likely contains plant/leaf content.
    """
    img = (img_array[0] * 255).astype(np.uint8)
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    # Green pixels: G > R and G > B by some margin
    green_mask = (g.astype(int) - r.astype(int) > 10) & \
                 (g.astype(int) - b.astype(int) > 10)
    green_ratio = green_mask.sum() / green_mask.size
    return green_ratio > threshold


def format_confidence(conf):
    """Format confidence as percentage string."""
    return f"{conf * 100:.1f}%"

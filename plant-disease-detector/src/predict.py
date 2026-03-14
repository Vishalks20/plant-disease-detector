"""
Prediction Module
==================
Load trained model and make predictions on single images or batches.

Usage (CLI):
    python src/predict.py --image path/to/leaf.jpg
    python src/predict.py --image path/to/leaf.jpg --top_k 5
"""

import sys
import json
import argparse
import numpy as np
from pathlib import Path
from PIL import Image

import tensorflow as tf

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config
from src.utils.helpers import (
    load_and_preprocess_image,
    preprocess_pil_image,
    load_class_indices,
    get_top_k_predictions,
    is_plant_image,
    format_confidence,
)
from src.utils.disease_info import get_disease_info, parse_class_name


# ─── Predictor class ─────────────────────────────────────────────────────────

class PlantDiseasePredictor:
    """Singleton-style predictor that loads the model once."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
            cls._instance._idx_to_class = None
        return cls._instance

    def load(self, model_path=None, class_indices_path=None):
        model_path = model_path or Config.MODEL_PATH
        class_indices_path = class_indices_path or Config.CLASS_INDICES

        if not Path(model_path).exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Download from the GitHub releases page or train a new model."
            )
        if not Path(class_indices_path).exists():
            raise FileNotFoundError(f"Class indices not found at {class_indices_path}.")

        self._model = tf.keras.models.load_model(str(model_path))
        self._idx_to_class = load_class_indices(str(class_indices_path))
        print(f"Model loaded: {model_path}")
        print(f"Classes: {len(self._idx_to_class)}")

    @property
    def is_loaded(self):
        return self._model is not None

    def predict_from_path(self, image_path: str, top_k: int = 5) -> dict:
        """Run prediction from an image file path."""
        img_array = load_and_preprocess_image(image_path, Config.IMG_SIZE)
        return self._run_inference(img_array, top_k)

    def predict_from_pil(self, pil_image: Image.Image, top_k: int = 5) -> dict:
        """Run prediction from a PIL Image object."""
        img_array = preprocess_pil_image(pil_image, Config.IMG_SIZE)
        return self._run_inference(img_array, top_k)

    def _run_inference(self, img_array: np.ndarray, top_k: int) -> dict:
        if not self.is_loaded:
            self.load()

        # Optional heuristic filter
        if not is_plant_image(img_array):
            return {
                "success": False,
                "error": "The uploaded image does not appear to contain plant/leaf content.",
            }

        predictions = self._model.predict(img_array, verbose=0)
        top_preds = get_top_k_predictions(predictions, self._idx_to_class, k=top_k)

        best = top_preds[0]
        class_name = best["class"]
        confidence = best["confidence"]

        if confidence < Config.CONFIDENCE_THRESHOLD:
            return {
                "success": False,
                "error": (
                    f"Low confidence ({format_confidence(confidence)}). "
                    "Please upload a clearer or closer leaf image."
                ),
                "top_predictions": top_preds,
            }

        plant, disease = parse_class_name(class_name)
        disease_info = get_disease_info(class_name)
        is_healthy = "healthy" in class_name.lower()

        return {
            "success": True,
            "class_name": class_name,
            "plant": plant,
            "disease": disease if not is_healthy else "Healthy",
            "confidence": round(confidence, 4),
            "confidence_pct": format_confidence(confidence),
            "is_healthy": is_healthy,
            "top_predictions": top_preds,
            "disease_info": {
                "common_name": disease_info["common_name"],
                "cause": disease_info["cause"],
                "symptoms": disease_info["symptoms"],
                "treatment": disease_info["treatment"],
                "prevention": disease_info["prevention"],
            },
        }


# ─── Singleton instance ───────────────────────────────────────────────────────
predictor = PlantDiseasePredictor()


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Predict plant disease from leaf image")
    parser.add_argument("--image", required=True, help="Path to leaf image")
    parser.add_argument("--top_k", type=int, default=5, help="Number of top predictions")
    parser.add_argument("--model", type=str, default=str(Config.MODEL_PATH))
    parser.add_argument("--classes", type=str, default=str(Config.CLASS_INDICES))
    args = parser.parse_args()

    predictor.load(args.model, args.classes)
    result = predictor.predict_from_path(args.image, top_k=args.top_k)

    if not result["success"]:
        print(f"\n❌ Prediction failed: {result.get('error', 'Unknown error')}")
        return

    print("\n" + "=" * 50)
    print("  Plant Disease Detection Result")
    print("=" * 50)
    print(f"  Plant   : {result['plant']}")
    print(f"  Disease : {result['disease']}")
    print(f"  Confidence: {result['confidence_pct']}")
    print(f"  Healthy : {'✅ Yes' if result['is_healthy'] else '❌ No'}")

    info = result["disease_info"]
    print(f"\n  Cause   : {info['cause']}")
    print(f"  Symptoms: {info['symptoms']}")

    if info["treatment"]:
        print("\n  Treatment:")
        for step in info["treatment"]:
            print(f"    • {step}")

    print("\n  Top Predictions:")
    for i, pred in enumerate(result["top_predictions"], 1):
        bar = "█" * int(pred["confidence"] * 20)
        print(f"    {i}. {pred['class']:<45} {format_confidence(pred['confidence'])} {bar}")

    print("=" * 50)


if __name__ == "__main__":
    main()

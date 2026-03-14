"""Flask API Routes for Plant Disease Detection."""

import os
import uuid
from pathlib import Path
from flask import Blueprint, request, jsonify, current_app
from PIL import Image
from werkzeug.utils import secure_filename

from src.utils.helpers import allowed_file
from src.predict import predictor

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _get_upload_folder():
    folder = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
    Path(folder).mkdir(parents=True, exist_ok=True)
    return folder


# ─── Health Check ─────────────────────────────────────────────────────────────

@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": predictor.is_loaded,
        "version": "1.0.0",
    })


# ─── Predict ──────────────────────────────────────────────────────────────────

@api_bp.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file in request. Use key 'image'."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    allowed = current_app.config.get("ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "webp"})
    if not allowed_file(file.filename, allowed):
        return jsonify({
            "success": False,
            "error": f"File type not allowed. Supported: {', '.join(allowed)}",
        }), 400

    try:
        # Ensure model is loaded
        if not predictor.is_loaded:
            predictor.load()

        # Read image directly from memory (no disk I/O required)
        pil_image = Image.open(file.stream)

        top_k = int(request.form.get("top_k", 5))
        result = predictor.predict_from_pil(pil_image, top_k=top_k)

        return jsonify(result), 200 if result["success"] else 422

    except Exception as e:
        current_app.logger.exception("Prediction error")
        return jsonify({"success": False, "error": str(e)}), 500


# ─── Classes List ─────────────────────────────────────────────────────────────

@api_bp.route("/classes", methods=["GET"])
def list_classes():
    """Return all supported plant/disease classes."""
    if not predictor.is_loaded:
        try:
            predictor.load()
        except Exception:
            return jsonify({"error": "Model not loaded"}), 503

    classes = list(predictor._idx_to_class.values()) if predictor._idx_to_class else []
    return jsonify({
        "total": len(classes),
        "classes": sorted(classes),
    })

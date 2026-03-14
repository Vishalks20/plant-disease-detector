"""
Plant Disease Detector — Flask Web Application
===============================================
Run with:
    python app.py                  # Development
    gunicorn app:app -b 0.0.0.0:5000  # Production
"""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pathlib import Path

from config import config, Config
from src.api.routes import api_bp


def create_app(env="development"):
    app = Flask(__name__)
    app.config.from_object(config[env])
    app.config["UPLOAD_FOLDER"] = str(Config.UPLOAD_FOLDER)
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH
    app.config["ALLOWED_EXTENSIONS"] = Config.ALLOWED_EXTENSIONS

    CORS(app)

    # Register API blueprint
    app.register_blueprint(api_bp)

    # ── Web UI Routes ──────────────────────────────────────────────────────
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/result")
    def result():
        return render_template("result.html")

    # ── Error Handlers ────────────────────────────────────────────────────
    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"success": False, "error": "File too large. Max size is 16MB."}), 413

    @app.errorhandler(404)
    def not_found(e):
        return render_template("index.html"), 404

    # ── Preload model on startup ──────────────────────────────────────────
    if Path(Config.MODEL_PATH).exists():
        from src.predict import predictor
        try:
            predictor.load()
            print("✅ Model preloaded successfully.")
        except Exception as ex:
            print(f"⚠️  Could not preload model: {ex}")
    else:
        print("⚠️  Model file not found. Download it from GitHub Releases.")
        print(f"   Expected: {Config.MODEL_PATH}")

    return app


app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

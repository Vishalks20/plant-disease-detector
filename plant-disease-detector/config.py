import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Paths
    DATA_DIR        = BASE_DIR / "data"
    RAW_DATA_DIR    = DATA_DIR / "raw" / "PlantVillage"
    PROCESSED_DIR   = DATA_DIR / "processed"
    MODELS_DIR      = BASE_DIR / "models"
    MODEL_PATH      = MODELS_DIR / "plant_disease_model.h5"
    CLASS_INDICES   = MODELS_DIR / "class_indices.json"

    # Image settings
    IMG_SIZE        = (224, 224)
    CHANNELS        = 3
    BATCH_SIZE      = 32

    # Training
    EPOCHS          = 25
    LEARNING_RATE   = 0.001
    VALIDATION_SPLIT = 0.1
    TEST_SPLIT      = 0.1

    # Flask
    SECRET_KEY      = os.environ.get("SECRET_KEY", "plant-disease-secret-key-2024")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER   = BASE_DIR / "static" / "uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Model
    NUM_CLASSES     = 38
    CONFIDENCE_THRESHOLD = 0.6  # Minimum confidence to report result

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}

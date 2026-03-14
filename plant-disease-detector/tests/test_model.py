"""Unit tests for model prediction logic."""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestHelpers:
    def test_format_confidence(self):
        from src.utils.helpers import format_confidence
        assert format_confidence(0.9732) == "97.3%"
        assert format_confidence(0.5) == "50.0%"
        assert format_confidence(1.0) == "100.0%"

    def test_allowed_file(self):
        from src.utils.helpers import allowed_file
        allowed = {"jpg", "jpeg", "png", "webp"}
        assert allowed_file("leaf.jpg", allowed) is True
        assert allowed_file("leaf.PNG", allowed) is True
        assert allowed_file("leaf.gif", allowed) is False
        assert allowed_file("noextension", allowed) is False

    def test_get_top_k_predictions(self):
        from src.utils.helpers import get_top_k_predictions
        probs = np.zeros((1, 5))
        probs[0] = [0.1, 0.05, 0.7, 0.1, 0.05]
        idx_to_class = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        top = get_top_k_predictions(probs, idx_to_class, k=3)
        assert top[0]["class"] == "C"
        assert abs(top[0]["confidence"] - 0.7) < 1e-6
        assert len(top) == 3

    def test_is_plant_image_green(self):
        from src.utils.helpers import is_plant_image
        # Mostly green image
        img = np.zeros((1, 100, 100, 3), dtype=np.float32)
        img[0, :, :, 1] = 0.8   # G
        img[0, :, :, 0] = 0.2   # R
        img[0, :, :, 2] = 0.2   # B
        assert is_plant_image(img) is True

    def test_is_plant_image_red(self):
        from src.utils.helpers import is_plant_image
        # Mostly red image
        img = np.zeros((1, 100, 100, 3), dtype=np.float32)
        img[0, :, :, 0] = 0.9   # R dominant
        assert is_plant_image(img) is False


class TestDiseaseInfo:
    def test_known_class(self):
        from src.utils.disease_info import get_disease_info
        info = get_disease_info("Tomato___Late_blight")
        assert info["common_name"] == "Tomato Late Blight"
        assert "cause" in info
        assert isinstance(info["treatment"], list)

    def test_unknown_class_fallback(self):
        from src.utils.disease_info import get_disease_info
        info = get_disease_info("Unknown___Class")
        assert "common_name" in info
        assert "treatment" in info

    def test_healthy_class(self):
        from src.utils.disease_info import get_disease_info
        info = get_disease_info("Tomato___healthy")
        assert info["treatment"] == []

    def test_parse_class_name(self):
        from src.utils.disease_info import parse_class_name
        plant, disease = parse_class_name("Tomato___Early_blight")
        assert plant == "Tomato"
        assert "Early" in disease

    def test_all_38_classes_covered(self):
        from src.utils.disease_info import DISEASE_INFO
        assert len(DISEASE_INFO) >= 38


class TestPredictor:
    def test_predictor_not_loaded(self):
        from src.predict import PlantDiseasePredictor
        p = PlantDiseasePredictor()
        assert isinstance(p.is_loaded, bool)

    def test_predictor_singleton(self):
        from src.predict import PlantDiseasePredictor
        p1 = PlantDiseasePredictor()
        p2 = PlantDiseasePredictor()
        assert p1 is p2

    def test_load_raises_without_model(self, tmp_path):
        from src.predict import PlantDiseasePredictor
        p = PlantDiseasePredictor.__new__(PlantDiseasePredictor)
        p._model = None
        p._idx_to_class = None
        with pytest.raises(FileNotFoundError):
            p.load(model_path=str(tmp_path / "nonexistent.h5"),
                   class_indices_path=str(tmp_path / "nonexistent.json"))

import pytest
import numpy as np
import cv2
from enhancex.ai.aae import AdaptiveAIEngine, CategoryDetector, QualityAnalyzer, MediaCategory, QualityDefect


def test_category_detector_general():
    detector = CategoryDetector()
    img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
    cat, conf = detector.detect(img)
    assert isinstance(cat, MediaCategory)
    assert 0.0 <= conf <= 1.0


def test_category_detector_document():
    detector = CategoryDetector()
    # Create white document page with text lines
    img = np.ones((500, 500, 3), dtype=np.uint8) * 240
    cv2.putText(img, "Sample Document Text Line", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    cv2.putText(img, "Second Line of Text", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    cat, conf = detector.detect(img)
    assert cat == MediaCategory.DOCUMENT


def test_quality_analyzer_blur_and_noise():
    analyzer = QualityAnalyzer()
    # Clean image vs blurred image
    clean = np.ones((200, 200, 3), dtype=np.uint8) * 128
    cv2.rectangle(clean, (50, 50), (150, 150), (255, 0, 0), -1)
    
    blurred = cv2.GaussianBlur(clean, (21, 21), 10)
    defects, metrics = analyzer.analyze(blurred)
    assert "blur_score" in metrics
    assert QualityDefect.BLUR in defects


def test_adaptive_ai_engine_auto_pipeline():
    engine = AdaptiveAIEngine()
    img = np.ones((300, 300, 3), dtype=np.uint8) * 40 # dark image
    analysis = engine.analyze(img)
    assert analysis.category == MediaCategory.NIGHT
    assert "low_light_boost" in analysis.recommended_pipeline or "denoise" in analysis.recommended_pipeline

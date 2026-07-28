import pytest
import numpy as np
from enhancex.image.resize import resize_image
from enhancex.image.sharpen import sharpen_image
from enhancex.image.denoise import denoise_image
from enhancex.image.color import apply_clahe, histogram_equalization, white_balance, adjust_color
from enhancex.image.pipeline import ImagePipeline


def test_resize_image(sample_image):
    resized = resize_image(sample_image, (512, 512))
    assert resized.shape == (512, 512, 3)

    scaled = resize_image(sample_image, 2.0)
    assert scaled.shape == (512, 512, 3)


def test_sharpen_image(sample_image):
    sharpened = sharpen_image(sample_image, strength=1.5, method="unsharp_mask")
    assert sharpened.shape == sample_image.shape
    laplacian = sharpen_image(sample_image, strength=1.0, method="laplacian")
    assert laplacian.shape == sample_image.shape


def test_denoise_image(sample_image):
    fastnl = denoise_image(sample_image, method="fastnl", h=5.0)
    assert fastnl.shape == sample_image.shape
    bilateral = denoise_image(sample_image, method="bilateral", h=5.0)
    assert bilateral.shape == sample_image.shape
    gaussian = denoise_image(sample_image, method="gaussian", h=5.0)
    assert gaussian.shape == sample_image.shape


def test_color_enhancements(sample_image):
    clahe_res = apply_clahe(sample_image, clip_limit=3.0)
    assert clahe_res.shape == sample_image.shape

    hist_res = histogram_equalization(sample_image)
    assert hist_res.shape == sample_image.shape

    wb_gw = white_balance(sample_image, method="gray_world")
    assert wb_gw.shape == sample_image.shape

    wb_wp = white_balance(sample_image, method="white_patch")
    assert wb_wp.shape == sample_image.shape

    adj_res = adjust_color(sample_image, brightness=10.0, contrast=1.2, gamma=1.1, saturation=1.2)
    assert adj_res.shape == sample_image.shape


def test_image_pipeline(sample_image):
    pipeline = ImagePipeline()
    res = pipeline.process(sample_image, use_clahe=True, use_white_balance=True, sharpen_strength=1.0, denoise_strength=2.0)
    assert res.shape == sample_image.shape

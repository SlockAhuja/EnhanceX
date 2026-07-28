import os
import pytest
from enhancex import VideoEnhancer, ImageEnhancer, Stabilizer, FrameInterpolator


def test_full_video_enhancer_pipeline(temp_media_dir):
    vid_in = temp_media_dir["video"]
    enh_out = os.path.join(temp_media_dir["dir"], "pipeline_enhanced.mp4")
    upscale_out = os.path.join(temp_media_dir["dir"], "pipeline_upscaled.mp4")

    enhancer = VideoEnhancer(device="cpu")

    # 1. Enhance
    res_enh = enhancer.enhance(vid_in, enh_out, sharpen=1.2, clahe=True)
    assert os.path.exists(res_enh)

    # 2. Upscale 2x
    res_upscale = enhancer.upscale(vid_in, upscale_out, scale=2, tile_size=64)
    assert os.path.exists(res_upscale)

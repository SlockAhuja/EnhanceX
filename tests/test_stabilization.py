import os
import pytest
from enhancex.video.stabilization import VideoStabilizer


def test_video_stabilizer(temp_media_dir):
    vid_path = temp_media_dir["video"]
    output_path = os.path.join(temp_media_dir["dir"], "stabilized.mp4")

    stabilizer = VideoStabilizer(smoothing_radius=5, border_mode="reflect")
    res = stabilizer.stabilize(vid_path, output_path)
    assert os.path.exists(res)

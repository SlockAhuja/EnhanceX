import os
import pytest
from enhancex.video.io import VideoReader, VideoWriter
from enhancex.video.scene import detect_scenes
from enhancex.video.trim import trim_video


def test_video_io(temp_media_dir):
    vid_path = temp_media_dir["video"]
    with VideoReader(vid_path) as reader:
        assert reader.fps > 0
        frames = list(reader)
        assert len(frames) == 10

    output_path = os.path.join(temp_media_dir["dir"], "written.mp4")
    with VideoWriter(output_path, 10.0, (128, 128)) as writer:
        for f in frames:
            writer.write(f)
    assert os.path.exists(output_path)


def test_scene_detection(temp_media_dir):
    vid_path = temp_media_dir["video"]
    scenes = detect_scenes(vid_path, threshold=5.0)
    assert isinstance(scenes, list)


def test_trim_video(temp_media_dir):
    vid_path = temp_media_dir["video"]
    output_path = os.path.join(temp_media_dir["dir"], "trimmed.mp4")
    res = trim_video(vid_path, output_path, start_time_sec=0.1, end_time_sec=0.5)
    assert os.path.exists(res)

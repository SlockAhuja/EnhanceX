import os
import sys
import pytest
from enhancex.cli.main import main, HAS_CLICK


def test_cli_help():
    if HAS_CLICK:
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "EnhanceX" in result.output
    else:
        assert True


def test_cli_enhance_image(temp_media_dir):
    img_in = temp_media_dir["image"]
    img_out = os.path.join(temp_media_dir["dir"], "cli_out.jpg")

    if HAS_CLICK:
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(main, ["enhance", img_in, img_out, "--sharpen", "1.2", "--clahe"])
        assert result.exit_code == 0
    else:
        # Direct main execution via sys.argv mock
        sys.argv = ["enhancex", "enhance", img_in, img_out, "--sharpen", "1.2", "--clahe"]
        try:
            main()
        except SystemExit:
            pass

    assert os.path.exists(img_out)


def test_cli_stabilize(temp_media_dir):
    vid_in = temp_media_dir["video"]
    vid_out = os.path.join(temp_media_dir["dir"], "cli_stab.mp4")

    if HAS_CLICK:
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(main, ["stabilize", vid_in, vid_out, "--smoothing", "5"])
        assert result.exit_code == 0
    else:
        sys.argv = ["enhancex", "stabilize", vid_in, vid_out, "--smoothing", "5"]
        try:
            main()
        except SystemExit:
            pass

    assert os.path.exists(vid_out)

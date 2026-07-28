from enhancex.video.io import VideoReader, VideoWriter
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Trim")


def trim_video(
    input_path: str,
    output_path: str,
    start_time_sec: float,
    end_time_sec: float
) -> str:
    """
    Trim video file between start_time_sec and end_time_sec.
    """
    with VideoReader(input_path) as reader:
        fps = reader.fps
        width, height = reader.width, reader.height
        start_frame = int(start_time_sec * fps)
        end_frame = int(end_time_sec * fps)

        with VideoWriter(output_path, fps, (width, height)) as writer:
            for idx, frame in enumerate(reader):
                if idx >= start_frame and idx <= end_frame:
                    writer.write(frame)
                elif idx > end_frame:
                    break

    logger.info(f"Trimmed video [{start_time_sec}s - {end_time_sec}s] saved to: {output_path}")
    return output_path

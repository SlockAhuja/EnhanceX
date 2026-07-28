import os
import cv2
import numpy as np


def generate_sample_assets(output_dir: str = "assets") -> dict:
    """Generates synthetic test image and test video for testing and benchmarks."""
    os.makedirs(output_dir, exist_ok=True)
    img_path = os.path.join(output_dir, "sample_input.jpg")
    video_path = os.path.join(output_dir, "sample_input.mp4")

    # Generate 512x512 gradient pattern test image with shapes
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    for y in range(512):
        for x in range(512):
            img[y, x] = [x % 256, y % 256, (x + y) % 256]
    cv2.circle(img, (256, 256), 100, (255, 255, 255), -1)
    cv2.putText(img, "EnhanceX Test Asset", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    cv2.imwrite(img_path, img)

    # Generate 3-second 30fps 640x480 test video with horizontal motion (for stabilization testing)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(video_path, fourcc, 30.0, (640, 480))
    for i in range(90):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cx = int(320 + 50 * np.sin(i * 0.2))
        cy = int(240 + 30 * np.cos(i * 0.2))
        cv2.circle(frame, (cx, cy), 60, (0, 255, 255), -1)
        cv2.putText(frame, f"Frame {i}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        writer.write(frame)
    writer.release()

    return {"image": img_path, "video": video_path}


if __name__ == "__main__":
    paths = generate_sample_assets()
    print(f"Generated sample assets: {paths}")

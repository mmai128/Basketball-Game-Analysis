from pathlib import Path
import subprocess

import cv2
from ultralytics import YOLO


MODEL_PATH = Path(__file__).parent / "best.pt"


def load_model():
    return YOLO(str(MODEL_PATH))


def predict_image(model, image, confidence):
    result = model.predict(
        source=image,
        conf=confidence,
        imgsz=640,
        verbose=False
    )[0]

    return cv2.cvtColor(
        result.plot(),
        cv2.COLOR_BGR2RGB
    )


def process_video(
    model,
    input_path,
    output_path,
    confidence,
    tracking=True,
    progress_callback=None
):

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise ValueError("Unable to open video.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    raw_path = Path(output_path).with_suffix(".avi")

    writer = cv2.VideoWriter(
        str(raw_path),
        cv2.VideoWriter_fourcc(*"MJPG"),
        fps,
        (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Video writer failed.")

    processed = 0

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if tracking:
                result = model.track(
                    frame,
                    persist=True,
                    tracker="bytetrack.yaml",
                    conf=confidence,
                    imgsz=640,
                    verbose=False
                )[0]

            else:
                result = model.predict(
                    frame,
                    conf=confidence,
                    imgsz=640,
                    verbose=False
                )[0]

            writer.write(result.plot())
            processed += 1

            if progress_callback and total > 0:
                progress_callback(
                    min(processed / total, 1.0)
                )

    finally:
        cap.release()
        writer.release()

    if processed == 0:
        raise RuntimeError("No frames processed.")

    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(raw_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path)
    ], check=True, capture_output=True)

    raw_path.unlink()

    return output_path
from pathlib import Path

import cv2
from ultralytics import YOLO

# 1. Load the most recent trained model.
project_root = Path(__file__).resolve().parent
weights_candidates = sorted(
    (project_root / "runs" / "detect").glob("train*/weights/best.pt"),
    key=lambda p: p.stat().st_mtime,
)
if not weights_candidates:
    raise FileNotFoundError("best.pt was not found. Please train the model first.")
model = YOLO(str(weights_candidates[-1]))

# 2. Run inference on an image.
# source can be an image path, video path, or camera index like "0".
source_image = project_root / "runs" / "test_image" / "1.jpg"
results = model.predict(source=str(source_image), show=False, save=False, conf=0.3)

result = results[0]
image = cv2.imread(str(source_image))
if image is None:
    raise FileNotFoundError(f"Cannot read image: {source_image}")

if result.boxes is None or len(result.boxes) == 0:
    print("No target detected")
else:
    confs = result.boxes.conf
    max_idx = int(confs.argmax().item())
    xyxy = result.boxes.xyxy[max_idx].tolist()
    x1, y1, x2, y2 = [int(v) for v in xyxy]
    x_center = (x1 + x2) / 2.0

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(
        image,
        f"conf={float(confs[max_idx]):.3f}",
        (x1, max(0, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
    )

    out_dir = project_root / "runs" / "detect" / "predict_best"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / source_image.name
    cv2.imwrite(str(out_path), image)

    print(f"Target detected, x={x_center:.2f}")
    print(f"Output saved to: {out_path}")

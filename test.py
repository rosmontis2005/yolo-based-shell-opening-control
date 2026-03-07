from ultralytics import YOLO
from pathlib import Path
import cv2

# 1. 加载你训练好的模型 (注意路径，runs文件夹是自动生成的)
# 这里的路径可能需要根据实际生成的文件夹修改，比如 runs/detect/train2/...
project_root = Path(__file__).resolve().parent
weights_candidates = sorted(
    (project_root / "runs" / "detect").glob("train*/weights/best.pt"),
    key=lambda p: p.stat().st_mtime,
)
if not weights_candidates:
    raise FileNotFoundError("未找到 best.pt，请先完成训练。")
model = YOLO(str(weights_candidates[-1]))

# 2. 进行预测
# source 可以是图片路径、视频路径，甚至填 '0' 调用摄像头
source_image = project_root / "runs" / "test_image" / "1.jpg"
results = model.predict(source=str(source_image), show=False, save=False, conf=0.3)

result = results[0]
image = cv2.imread(str(source_image))
if image is None:
    raise FileNotFoundError(f"无法读取图片: {source_image}")

if result.boxes is None or len(result.boxes) == 0:
    print("未检测到目标")
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

    print(f"检测到目标，x={x_center:.2f}")
    print(f"结果已保存: {out_path}")

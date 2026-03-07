from pathlib import Path

from ultralytics import YOLO

# 1. Load the base model.
# yolo26n.pt is lightweight and fast, good for first-time training runs.
# If your GPU is stronger, you can switch to larger variants.
model = YOLO("yolo26n.pt")

# 2. Start training.
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    data_yaml = project_root / "data.yaml"

    # data: dataset config file
    # epochs: number of training epochs
    # imgsz: image size, commonly 640
    # batch: reduce this if GPU memory is limited
    # device: 0 for the first GPU, or "cpu" if no GPU is available
    # workers: keep low on Windows to avoid dataloader issues
    model.train(
        data=str(data_yaml),
        epochs=500,
        imgsz=640,
        batch=8,
        workers=0,
        device=0,
    )

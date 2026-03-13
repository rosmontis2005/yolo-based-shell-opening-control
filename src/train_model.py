from ultralytics import YOLO

from project_paths import BASE_MODEL_WEIGHTS, DEFAULT_DATA_CONFIG, TRAINING_OUTPUT_DIR


def main() -> None:
    if not BASE_MODEL_WEIGHTS.exists():
        raise FileNotFoundError(
            f"Base model weights not found: {BASE_MODEL_WEIGHTS}. Please place yolo26n.pt in models/."
        )

    model = YOLO(str(BASE_MODEL_WEIGHTS))

    # data: dataset config file
    # epochs: number of training epochs
    # imgsz: image size, commonly 640
    # batch: reduce this if GPU memory is limited
    # device: 0 for the first GPU, or "cpu" if no GPU is available
    # workers: keep low on Windows to avoid dataloader issues
    model.train(
        data=str(DEFAULT_DATA_CONFIG),
        epochs=500,
        imgsz=640,
        batch=8,
        workers=0,
        device=0,
        project=str(TRAINING_OUTPUT_DIR),
        name="train",
    )


if __name__ == "__main__":
    main()

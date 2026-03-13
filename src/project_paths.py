from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS_DIR = PROJECT_ROOT / "configs"
DATASET_DIR = PROJECT_ROOT / "datasets" / "shell_opening"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

DEFAULT_DATA_CONFIG = CONFIGS_DIR / "data.yaml"
BASE_MODEL_WEIGHTS = MODELS_DIR / "yolo26n.pt"
TRAINING_OUTPUT_DIR = OUTPUTS_DIR / "runs" / "detect"
CAPTURES_DIR = OUTPUTS_DIR / "captures"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"
CAMERA_SCANS_DIR = OUTPUTS_DIR / "camera_scans"


def latest_best_weights() -> Path:
    candidates = sorted(
        TRAINING_OUTPUT_DIR.glob("train*/weights/best.pt"),
        key=lambda path: path.stat().st_mtime,
    )
    if not candidates:
        raise FileNotFoundError(
            f"best.pt was not found under {TRAINING_OUTPUT_DIR}. Please train the model first."
        )
    return candidates[-1]

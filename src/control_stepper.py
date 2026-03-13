from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from project_paths import PROJECT_ROOT

SCRIPT_DIR = Path(__file__).resolve().parent


def import_pyserial():
    try:
        import serial
        from serial.tools import list_ports
    except ImportError as exc:
        raise RuntimeError(
            "pyserial is required for serial communication. Install it with: pip install pyserial"
        ) from exc

    return serial, list_ports


def run_detection(detect_script: Path, camera_index: int, conf: float) -> dict:
    command = [
        sys.executable,
        str(detect_script),
        "--camera-index",
        str(camera_index),
        "--conf",
        str(conf),
        "--json",
    ]
    completed = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "Unknown error"
        raise RuntimeError(f"Detection failed: {message}")

    stdout = completed.stdout.strip()
    if not stdout:
        raise RuntimeError("Detection failed: no JSON output")

    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue

    raise RuntimeError(f"Detection output does not contain valid JSON: {stdout}")


def map_detection_to_target(detection: dict, fixed_target: int) -> tuple[int, float | None]:
    detected = bool(detection.get("detected", False))
    raw_value = detection.get("x_center")
    raw_float = float(raw_value) if raw_value is not None else None

    if not detected or raw_float is None:
        return 0, raw_float

    # Placeholder mapping (as requested): detected target is currently fixed to 1.
    return int(fixed_target), raw_float


def send_target_position(port: str, baud: int, target: int) -> tuple[str, str]:
    serial, _ = import_pyserial()
    command = f"POS:{target}\n"

    with serial.Serial(port=port, baudrate=baud, timeout=2) as ser:
        # Many Arduino boards reset after opening serial.
        time.sleep(2)
        ser.reset_input_buffer()
        ser.write(command.encode("utf-8"))
        ser.flush()
        ack = ser.readline().decode("utf-8", errors="replace").strip()

    return command.strip(), ack


def print_ports() -> None:
    _, list_ports = import_pyserial()
    ports = list(list_ports.comports())
    if not ports:
        print("No serial ports found")
        return

    print("Available serial ports:")
    for port in ports:
        print(f"- {port.device}: {port.description}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run detect_once.py once and send mapped target position to Arduino stepper."
    )
    parser.add_argument("--port", help="Serial port, e.g. COM3 or /dev/cu.usbmodemXXXX")
    parser.add_argument("--baud", type=int, default=9600)
    parser.add_argument("--camera-index", type=int, default=1)
    parser.add_argument("--conf", type=float, default=0.1)
    parser.add_argument("--detect-script", default="detect_once.py")
    parser.add_argument(
        "--fixed-target",
        type=int,
        default=1,
        help="Mapped stepper target when detection is successful (temporary fixed mapping)",
    )
    parser.add_argument(
        "--manual-position",
        type=int,
        help="Skip detection and send this absolute position directly",
    )
    parser.add_argument("--dry-run", action="store_true", help="Run detection/mapping only")
    parser.add_argument(
        "--list-ports",
        action="store_true",
        help="List serial ports and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_ports:
        print_ports()
        return

    detection = None
    raw_value = None

    if args.manual_position is None:
        detect_script = Path(args.detect_script)
        if not detect_script.is_absolute():
            detect_script = (SCRIPT_DIR / detect_script).resolve()
        if not detect_script.exists():
            raise FileNotFoundError(f"Detection script not found: {detect_script}")

        detection = run_detection(
            detect_script=detect_script,
            camera_index=args.camera_index,
            conf=args.conf,
        )
        target, raw_value = map_detection_to_target(
            detection=detection,
            fixed_target=args.fixed_target,
        )
    else:
        target = int(args.manual_position)

    if detection is not None:
        print(
            f"Detection result: detected={bool(detection.get('detected', False))}, "
            f"confidence={detection.get('confidence')}, x_center={raw_value}"
        )
        print(f"Input frame: {detection.get('input_frame')}")
        if detection.get("output_frame"):
            print(f"Output frame: {detection['output_frame']}")

    print(f"Mapped target position: {target}")

    if args.dry_run:
        print("Dry-run mode: no serial command sent")
        return

    if not args.port:
        raise ValueError("--port is required unless --dry-run or --list-ports is used")

    command, ack = send_target_position(port=args.port, baud=args.baud, target=target)
    print(f"Sent command: {command}")
    if ack:
        print(f"Arduino reply: {ack}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(exc)
        raise SystemExit(1)

# YOLO-Based Shell Opening Control

这是一个基于 YOLO 的视觉检测项目，用来识别目标后联动 Arduino 舵机做开壳控制验证。

当前项目已经按职责重新整理：
- `src/` 放 Python 源码
- `configs/` 放配置文件
- `docs/` 放说明文档
- `arduino/` 放 Arduino 程序
- `datasets/`、`models/`、`outputs/` 放本地数据、权重和运行产物

其中 `datasets/`、`models/`、`outputs/` 默认不上传 GitHub，适合本地开发和调试。

## 目录结构

```text
yolo-based-shell-opening-control/
├── arduino/
│   ├── servo_detect_test/
│   ├── stepper_basic_test/
│   └── stepper_detect_control/
├── configs/
│   └── data.yaml
├── datasets/
│   └── shell_opening/
│       ├── images/
│       └── labels/
├── docs/
│   ├── arduino_servo_test.md
│   └── arduino_stepper_test.md
├── models/
│   └── yolo26n.pt
├── outputs/
│   ├── camera_scans/
│   ├── captures/
│   ├── predictions/
│   └── runs/
├── src/
│   ├── camera_scan.py
│   ├── control_servo.py
│   ├── control_stepper.py
│   ├── detect_once.py
│   ├── project_paths.py
│   └── train_model.py
├── .gitignore
├── README.md
└── requirements.txt
```

## 环境准备

建议使用 Python 3.10 或以上版本。

安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 数据与模型

### 数据集目录

训练配置文件在 [configs/data.yaml](/Users/rosmontis/Projects/CV/yolo-based-shell-opening-control/configs/data.yaml)，当前约定的数据集结构为：

```text
datasets/shell_opening/
├── images/
│   ├── train/
│   └── val/
└── labels/
    ├── train/
    └── val/
```

### 基础权重

请把基础模型权重放在：

```text
models/yolo26n.pt
```

训练完成后，最佳权重会默认输出到：

```text
outputs/runs/detect/train/weights/best.pt
```

## 常用命令

### 1. 训练模型

```bash
python3 src/train_model.py
```

说明：
- 训练脚本默认读取 `configs/data.yaml`
- 当前默认 `device=0`，如果你没有可用 GPU，可以把 [src/train_model.py](/Users/rosmontis/Projects/CV/yolo-based-shell-opening-control/src/train_model.py) 里的 `device=0` 改成 `"cpu"`

### 2. 单次拍照并检测

```bash
python3 src/detect_once.py --json
```

可选参数示例：

```bash
python3 src/detect_once.py --camera-index 1 --conf 0.1
```

运行后会：
- 从摄像头读取一帧
- 使用最新训练得到的 `best.pt` 做检测
- 把输入图保存到 `outputs/captures/detection/`
- 把检测结果图保存到 `outputs/predictions/`

### 3. 扫描本机可用摄像头

```bash
python3 src/camera_scan.py
```

运行后会：
- 依次探测摄像头索引 `0-9`
- 把抓拍帧保存到 `outputs/camera_scans/frames/`
- 把汇总结果保存到 `outputs/camera_scans/`

### 4. 联动 Arduino 舵机

先查看可用串口：

```bash
python3 src/control_servo.py --list-ports
```

执行一次检测并发送串口命令：

```bash
python3 src/control_servo.py --port COM3 --baud 9600 --camera-index 1
```

只检测，不发串口：

```bash
python3 src/control_servo.py --dry-run --camera-index 1
```

详细硬件说明见 [docs/arduino_servo_test.md](/Users/rosmontis/Projects/CV/yolo-based-shell-opening-control/docs/arduino_servo_test.md)。

### 5. 联动 Arduino 丝杆步进电机

先查看可用串口：

```bash
python3 src/control_stepper.py --list-ports
```

执行一次检测并发送目标位置（当前映射临时固定为 1）：

```bash
python3 src/control_stepper.py --port COM3 --baud 9600 --camera-index 1
```

只检测与映射，不发串口：

```bash
python3 src/control_stepper.py --dry-run --camera-index 1
```

跳过检测，直接发送手动目标位置：

```bash
python3 src/control_stepper.py --port COM3 --manual-position 1200
```

详细硬件说明见 [docs/arduino_stepper_test.md](/Users/rosmontis/Projects/CV/yolo-based-shell-opening-control/docs/arduino_stepper_test.md)。

## 路径管理说明

项目中的路径已经集中到 [src/project_paths.py](/Users/rosmontis/Projects/CV/yolo-based-shell-opening-control/src/project_paths.py)。

如果以后你还想继续整理目录，优先修改这个文件，而不是去多个脚本里手动搜索字符串。

## Git 管理建议

以下内容建议只保留在本地，不上传 GitHub：
- 原始数据集图片和标注
- `.cache` 文件
- 模型权重 `.pt`
- 训练输出和推理截图
- IDE 配置和系统缓存文件

这些规则已经写入 [.gitignore](/Users/rosmontis/Projects/CV/yolo-based-shell-opening-control/.gitignore)。

## 后续建议

如果你想继续把工程习惯做得更稳，我建议下一步再补这几项：
- 增加 `scripts/` 目录，专门放启动脚本
- 增加 `tests/` 目录，至少先给路径工具和参数解析写一点基础测试
- 把训练参数抽到独立配置文件，避免每次改源码
- 补一个数据准备文档，记录标注格式和命名规则

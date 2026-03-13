# YOLO 检测结果驱动丝杆步进电机（位置模式）

## 1. 结构说明
Arduino 不能直接运行 `src/detect_once.py`，推荐结构如下：

- 电脑运行 Python：执行检测，得到 `x_center`
- 电脑做映射：`x_center -> 目标位置`
- 电脑串口发送：`POS:<整数>`
- Arduino 接收后驱动步进电机移动到绝对位置

本仓库新增了：
- `arduino/stepper_basic_test/stepper_basic_test.ino`：纯硬件往返测试
- `arduino/stepper_detect_control/stepper_detect_control.ino`：串口位置控制
- `src/control_stepper.py`：检测 + 映射 + 串口发送

## 2. 建议接线（UNO + A4988/TMC）
- `D2 -> STEP`
- `D3 -> DIR`
- `D4 -> EN`
- `GND -> GND`（Arduino 与驱动器共地）

注意：
- 驱动器电机电源请使用独立供电，不要直接由 Arduino 5V 供电电机
- 若方向反了，可交换电机线序或反转 `DIR` 逻辑

## 3. 脚本 1：纯硬件测试
烧录：`arduino/stepper_basic_test/stepper_basic_test.ino`

现象：
- 电机会按固定步数往返运动
- 串口监视器（9600）会输出当前位置 `POS:<value>`

用途：
- 验证接线、使能、方向、脉冲是否正常

## 4. 脚本 2：实际工作（串口位置）
烧录：`arduino/stepper_detect_control/stepper_detect_control.ino`

串口协议（9600）：
- `POS:<整数>`：移动到绝对位置
- `GET`：返回当前 `POS:<value>`
- `HOME`：回到 0
- `PING`：返回 `PONG`

上位机默认发送 `POS:<目标值>`，Arduino 回应 `OK:POS:<当前值>`。

## 5. Python 端调用
先列出可用串口（确认数据端口）：

```bash
python3 src/control_stepper.py --list-ports
```

一次检测并联动（当前映射临时固定为 `1`）：

```bash
python3 src/control_stepper.py --port COM3 --baud 9600 --camera-index 1
```

如果是 macOS/Linux，端口一般类似：

```bash
python3 src/control_stepper.py --port /dev/cu.usbmodem14101 --baud 9600 --camera-index 1
```

仅测试映射，不发串口：

```bash
python3 src/control_stepper.py --dry-run --camera-index 1
```

跳过检测，手动发目标位置（用于串口链路测试）：

```bash
python3 src/control_stepper.py --port COM3 --manual-position 1200
```

## 6. 端口与波特率检查结果
当前代码端口设置是正确且一致的：
- Arduino 两个步进脚本都使用 `Serial.begin(9600)`
- `src/control_stepper.py` 默认 `--baud 9600`
- 串口端口不是写死的，运行时通过 `--port` 传入，适配不同电脑

## 7. 目前映射逻辑
`src/control_stepper.py` 已从 `detect_once.py` 获取 `x_center`，并走映射函数。

按你当前要求，映射结果临时固定为：
- 检测到目标：位置 `1`
- 未检测到目标：位置 `0`

后续可把映射改成线性或分段函数，例如：`x_center` 映射到 `[0, MAX_POSITION]`。

# YOLO 检测结果驱动 Arduino 舵机（0° / 90°）

## 1. 结论先说
Arduino 不能直接运行或调用 `test.py`。

推荐结构是：
- 电脑运行 Python（拍照 + YOLO 检测）
- 电脑通过串口给 Arduino 发一个很短的命令
- Arduino 收到命令后控制舵机

本仓库已经准备好：
- `test.py`：支持 `--json` 输出检测结果
- `control_servo.py`：运行检测并把结果发给 Arduino
- `arduino/servo_detect_test/servo_detect_test.ino`：Arduino 舵机控制程序

## 2. Arduino 接线（以 UNO + SG90 为例）
- 舵机信号线（橙/黄） -> D9
- 舵机 VCC（红） -> 5V（建议外部 5V 供电）
- 舵机 GND（棕/黑） -> GND

注意：如果用外部 5V 给舵机供电，外部电源 GND 必须和 Arduino GND 共地。

## 3. 烧录 Arduino 程序
1. 打开 Arduino IDE
2. `File -> Open`，选择：
   `arduino/servo_detect_test/servo_detect_test.ino`
3. `Tools -> Board` 选择你的开发板（如 Arduino Uno）
4. `Tools -> Port` 选择对应串口（如 COM3）
5. 点击 `Upload`
6. 打开串口监视器（9600 波特率），上电后看到 `READY` 说明程序正常

## 4. 电脑端安装依赖
在项目根目录执行：

```powershell
pip install pyserial ultralytics opencv-python
```

## 5. 先测试检测脚本（可选）
```powershell
python test.py --json
```

会输出类似：
```json
{"detected": true, "x_center": 321.5, "confidence": 0.8821, ...}
```

## 6. 一键联动测试
### 6.1 查看串口
```powershell
python control_servo.py --list-ports
```

### 6.2 运行一次检测并控制舵机
```powershell
python control_servo.py --port COM3 --baud 9600 --camera-index 1
```

逻辑：
- 检测到目标 -> 发送 `1` -> 舵机转到 90°
- 未检测到目标 -> 发送 `0` -> 舵机回到 0°

### 6.3 只做检测不发串口
```powershell
python control_servo.py --dry-run --camera-index 1
```

## 7. 你问的“C++ 程序能调用 test.py 吗？”
可以，但那是“电脑上的 C++ 程序”调用 Python 进程，不是“Arduino 上的 C++”。

当前方案已经是最简、最稳定的验证路径：
- 算法在 Python
- 控制在 Arduino
- 中间用串口协议 `0/1`

后续如果你想，我可以再帮你扩展成连续循环版本（每隔 N 秒检测一次并控制舵机）。

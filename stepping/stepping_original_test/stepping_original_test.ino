// ===== TB6600 + Arduino 简单往返测试 =====
// 接线示例：
// Arduino D3 -> TB6600 PUL+
// Arduino D2 -> TB6600 DIR+
// Arduino D4 -> TB6600 ENA+   （可选，不接也行）
// Arduino GND -> TB6600 PUL- / DIR- / ENA-
//
// 注意：你的TB6600接法可能和这里不同，若驱动器不转，先检查共阴/共阳接法。

const int STEP_PIN = 3;   // 脉冲信号 PUL
const int DIR_PIN  = 2;   // 方向信号 DIR
const int EN_PIN   = 4;   // 使能信号 ENA（可选）

// ===== 可调参数 =====
const long TRAVEL_STEPS = 100000;   // 左右端点之间的步数差，先设小一点测试
const int PULSE_US = 10;         // 脉冲宽度，越小转得越快；先用 500 比较稳
const int END_PAUSE_MS = 1000;    // 到端点后的停顿时间

void stepMotor(long steps, bool dir) {
  digitalWrite(DIR_PIN, dir);

  for (long i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(PULSE_US);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(PULSE_US);
  }
}

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);

  // TB6600 常见情况：ENA 为低电平使能
  digitalWrite(EN_PIN, LOW);

  // 上电稳定一下
  delay(2000);
}

void loop() {
  // 向右走
  stepMotor(TRAVEL_STEPS, true);
  delay(END_PAUSE_MS);

  // 向左走
  stepMotor(TRAVEL_STEPS, false);
  delay(END_PAUSE_MS);
}
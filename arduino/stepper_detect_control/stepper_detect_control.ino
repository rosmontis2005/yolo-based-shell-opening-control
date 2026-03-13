// Production stepper script:
// - Receives serial command: POS:<target>
// - Moves screw stepper to absolute target position
// - Replies with ACK for host-side verification

const int STEP_PIN = 2;
const int DIR_PIN = 3;
const int EN_PIN = 4;

const bool ENABLE_LOW = true;   // A4988/TMC style enable pin: LOW = enabled
const unsigned int STEP_PULSE_US = 700;

const long MIN_POSITION = 0;
const long MAX_POSITION = 20000;

String incoming;
long currentPosition = 0;

void setup() {
  Serial.begin(9600);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);

  enableDriver(true);
  Serial.println("READY");
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (incoming.length() > 0) {
        handleCommand(incoming);
        incoming = "";
      }
    } else {
      incoming += c;
    }
  }
}

void enableDriver(bool enabled) {
  if (ENABLE_LOW) {
    digitalWrite(EN_PIN, enabled ? LOW : HIGH);
  } else {
    digitalWrite(EN_PIN, enabled ? HIGH : LOW);
  }
}

void pulseStep() {
  digitalWrite(STEP_PIN, HIGH);
  delayMicroseconds(STEP_PULSE_US);
  digitalWrite(STEP_PIN, LOW);
  delayMicroseconds(STEP_PULSE_US);
}

void moveTo(long targetPosition) {
  if (targetPosition < MIN_POSITION) {
    targetPosition = MIN_POSITION;
  } else if (targetPosition > MAX_POSITION) {
    targetPosition = MAX_POSITION;
  }

  long delta = targetPosition - currentPosition;
  if (delta == 0) {
    return;
  }

  digitalWrite(DIR_PIN, delta > 0 ? HIGH : LOW);

  long steps = (delta > 0) ? delta : -delta;
  for (long i = 0; i < steps; ++i) {
    pulseStep();
  }

  currentPosition = targetPosition;
}

bool parseLongStrict(String text, long &valueOut) {
  text.trim();
  if (text.length() == 0) {
    return false;
  }

  bool negative = false;
  int idx = 0;
  if (text[0] == '-' || text[0] == '+') {
    negative = (text[0] == '-');
    idx = 1;
    if (idx >= text.length()) {
      return false;
    }
  }

  long value = 0;
  for (; idx < text.length(); ++idx) {
    char c = text[idx];
    if (c < '0' || c > '9') {
      return false;
    }
    value = value * 10 + (c - '0');
  }

  valueOut = negative ? -value : value;
  return true;
}

void handleCommand(String cmd) {
  cmd.trim();

  if (cmd == "PING") {
    Serial.println("PONG");
    return;
  }

  if (cmd == "GET") {
    Serial.print("POS:");
    Serial.println(currentPosition);
    return;
  }

  if (cmd == "HOME") {
    moveTo(0);
    Serial.print("OK:HOME:");
    Serial.println(currentPosition);
    return;
  }

  if (cmd.startsWith("POS:")) {
    String valueText = cmd.substring(4);
    long target = 0;
    if (!parseLongStrict(valueText, target)) {
      Serial.print("ERR:BAD_POS:");
      Serial.println(valueText);
      return;
    }

    moveTo(target);
    Serial.print("OK:POS:");
    Serial.println(currentPosition);
    return;
  }

  Serial.print("ERR:UNKNOWN:");
  Serial.println(cmd);
}

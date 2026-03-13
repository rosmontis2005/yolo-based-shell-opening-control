// Basic stepper smoke test for screw drive:
// - Moves forward by TEST_TRAVEL_STEPS
// - Moves backward by TEST_TRAVEL_STEPS
// Confirm wiring, direction and stable stepping before vision integration.

const int STEP_PIN = 2;
const int DIR_PIN = 3;
const int EN_PIN = 4;

const bool ENABLE_LOW = true;   // A4988/TMC style enable pin: LOW = enabled
const unsigned int STEP_PULSE_US = 700;
const long TEST_TRAVEL_STEPS = 800;

long currentPosition = 0;

void setup() {
  Serial.begin(9600);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);

  enableDriver(true);
  Serial.println("STEPPER_BASIC_READY");
}

void loop() {
  moveRelative(TEST_TRAVEL_STEPS);
  delay(800);

  moveRelative(-TEST_TRAVEL_STEPS);
  delay(800);
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

void moveRelative(long delta) {
  if (delta == 0) {
    return;
  }

  digitalWrite(DIR_PIN, delta > 0 ? HIGH : LOW);

  long steps = (delta > 0) ? delta : -delta;
  for (long i = 0; i < steps; ++i) {
    pulseStep();
  }

  currentPosition += delta;
  Serial.print("POS:");
  Serial.println(currentPosition);
}

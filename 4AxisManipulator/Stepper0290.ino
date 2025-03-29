#define STEP_PIN 3   // Pin connected to the STEP pin on the A4988
#define DIR_PIN 4    // Pin connected to the DIR pin on the A4988
#define ENABLE_PIN 5 // Optional pin to enable/disable the stepper (can be left out if not needed)

int stepsPerRevolution = 200; // Number of steps for a full rotation (1.8° per step)
int currentSteps = 0;         // Current position of the motor in steps
float stepsPerDegree = 360/stepsPerRevolution ; // Steps per degree (200 steps / 360°)

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  digitalWrite(ENABLE_PIN, LOW); // Enable the motor

  // // Move to 0 degrees
  // moveToAngle(0);
  // delay(1000);
  // Move to 90 degrees
  moveToAngle(90);
  delay(1000);

}

void loop() {
  // Do nothing; motor should stop at 90 degrees
}
void moveToAngle(int targetAngle) {
  float targetSteps = targetAngle / stepsPerDegree;
  int stepsToMove = targetSteps - currentSteps;

  // direction
  if (stepsToMove > 0) {
    digitalWrite(DIR_PIN, HIGH); // Clockwise
  } else {
    digitalWrite(DIR_PIN, LOW);  // Counterclockwise
    stepsToMove = -stepsToMove;  //  positive steps for movement
  }

  // Move the motor the required number of steps
  for (int i = 0; i < stepsToMove; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000); 
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000); 
  }
  currentSteps = targetSteps;
}

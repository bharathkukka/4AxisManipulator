// Defines pins for step and direction
#define stepPin 3
#define dirPin 4 

// Defines the delay between steps (in microseconds)
int stepDelay = 700; // Time delay between steps (adjust for speed)

void setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin, OUTPUT); 
  pinMode(dirPin, OUTPUT);
}

void loop() {
  // Rotate in one direction
  digitalWrite(dirPin, HIGH); // Set direction to clockwise
  // Makes 400 pulses for two full cycle rotations (200 steps per revolution)
  for(int x = 0; x < 400; x++) {
    stepMotor(); // Call function to step the motor
  }
  delay(1000); // One second delay between movements
  
  // Rotate in the opposite direction
  digitalWrite(dirPin, LOW); // Set direction to counterclockwise
  // Makes 800 pulses for four full cycle rotations (200 steps per revolution)
  for(int x = 0; x < 800; x++) {
    stepMotor(); // Call function to step the motor
  }
  
  delay(1000); // One second delay before repeating the loop
}

// Function to step the motor
void stepMotor() {
  digitalWrite(stepPin, HIGH); 
  delayMicroseconds(stepDelay); // Delay for step timing
  digitalWrite(stepPin, LOW); 
  delayMicroseconds(stepDelay); // Delay for step timing
}
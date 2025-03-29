#include <Servo.h>
#include <AccelStepper.h>

// Pin Definitions
#define SERVO1_PIN 2
#define SERVO2_PIN 3
#define STEP1_PIN 4
#define DIR1_PIN 5
#define STEP2_PIN 6
#define DIR2_PIN 7
#define STEP3_PIN 8
#define DIR3_PIN 9

// Servo Objects
Servo servo1, servo2;

// Stepper Motor Objects
AccelStepper stepper1(AccelStepper::DRIVER, STEP1_PIN, DIR1_PIN);
AccelStepper stepper2(AccelStepper::DRIVER, STEP2_PIN, DIR2_PIN);
AccelStepper stepper3(AccelStepper::DRIVER, STEP3_PIN, DIR3_PIN);

void initialize_motors() {
    stepper1.setMaxSpeed(100); //  max speed (steps per second)
    stepper1.setAcceleration(50); // acceleration (steps per second^2)

    stepper2.setMaxSpeed(100);
    stepper2.setAcceleration(50);

    stepper3.setMaxSpeed(100);
    stepper3.setAcceleration(50);
}

// Move a Servo to a Specified Angle
void move_servo(Servo &servo, int angle) {
    servo.write(angle); // Set the servo angle
    delay(500);         // Allow time for the servo to reach the position
}

// Move a Stepper Motor to a Specified Angle
void move_stepper(AccelStepper &stepper, int current_steps[], int motor_id, int target_angle) {
    int steps_per_revolution = 200;  // Assumes 1.8° step angle
    int target_steps = (target_angle % 360) * steps_per_revolution / 360;

    stepper.moveTo(target_steps); // Command the motor to move to target_steps
    while (stepper.distanceToGo() != 0) {
        stepper.run(); // Move the stepper motor smoothly
    }

    current_steps[motor_id] = target_steps; // Update the current position
}

// Process Incoming Commands
void process_command(String command, int current_steps[]) {
    int motor_id, angle;

    // Home all motors
    if (command.startsWith("HOM")) {
        move_servo(servo1, 90);
        move_servo(servo2, 90);
        move_stepper(stepper1, current_steps, 0, 0);
        move_stepper(stepper2, current_steps, 1, 0);
        move_stepper(stepper3, current_steps, 2, 0);
        return;
    }

    // Process motor movement commands
    if (command.startsWith("M")) {
        motor_id = command.substring(1, 2).toInt(); // Extract motor ID
        angle = command.substring(2).toInt();       // Extract angle

        // Control the respective motor
        if (motor_id == 1) move_stepper(stepper1, current_steps, 0, angle);
        else if (motor_id == 2) move_stepper(stepper2, current_steps, 1, angle);
        else if (motor_id == 3) move_stepper(stepper3, current_steps, 2, angle);
        else if (motor_id == 4) move_servo(servo1, angle);
        else if (motor_id == 5) move_servo(servo2, angle);
    }
}

// Arduino Setup Function
void setup() {
    // Attach servos
    servo1.attach(SERVO1_PIN);
    servo2.attach(SERVO2_PIN);

    // Initialize steppers
    initialize_motors();

    // Initialize UART
    Serial.begin(9600);
}

// Arduino Loop Function
void loop() {
    String command = "";
    static int current_steps[3] = {0, 0, 0}; // Track step positions for 3 motors

    // Read command from Serial until '\n'
    while (Serial.available() > 0) {
        char c = Serial.read();
        if (c == '\n') break; // End of command
        command += c;         // Append to command string
    }

    // Process the received command
    if (command.length() > 0) {
        process_command(command, current_steps);
        delay(500); // Optional delay
    }
}

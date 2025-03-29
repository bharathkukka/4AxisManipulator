#include <Servo.h>

// Pin Definitions
#define SERVO1_PIN 10
#define SERVO2_PIN 11
#define STEP1_PIN 4
#define DIR1_PIN 5
#define STEP2_PIN 6
#define DIR2_PIN 7
#define STEP3_PIN 8
#define DIR3_PIN 9

// Servo Objects
Servo servo1, servo2;

// Stepper Motor Steps Tracking
int current_steps[3] = {0, 0, 0};

// Move a Servo to a Specified Angle
void move_servo(Servo &servo, int angle) {
    servo.write(angle); // Set the servo angle
    delay(500);         // Allow time for the servo to reach the position
}

// Move a Stepper Motor to a Specified Angle
void move_stepper(int step_pin, int dir_pin, int *current_steps, int target_angle) {
    int steps_per_revolution = 200;  // Assumes 1.8° step angle
    int target_steps = (target_angle % 360) * steps_per_revolution / 360;
    int step_difference = target_steps - *current_steps;

    // Optimize step direction
    if (step_difference > steps_per_revolution / 2)
        step_difference -= steps_per_revolution;
    else if (step_difference < -steps_per_revolution / 2)
        step_difference += steps_per_revolution;

    digitalWrite(dir_pin, (step_difference > 0) ? HIGH : LOW); // Set direction
    step_difference = abs(step_difference);

    // Execute the steps
    for (int i = 0; i < step_difference; i++) {
        digitalWrite(step_pin, HIGH);
        delayMicroseconds(1000); // Adjust speed if necessary
        digitalWrite(step_pin, LOW);
        delayMicroseconds(1000);
    }

    *current_steps = target_steps; // Update the current step position
}

// Process Incoming Commands
void process_command(String command) {
    int motor_id, angle;

    // Home all motors
    if (command.startsWith("HOM")) {
        move_servo(servo1, 90);
        move_servo(servo2, 90);
        move_stepper(STEP1_PIN, DIR1_PIN, &current_steps[0], 0);
        move_stepper(STEP2_PIN, DIR2_PIN, &current_steps[1], 0);
        move_stepper(STEP3_PIN, DIR3_PIN, &current_steps[2], 0);
        return;
    }

    // Process motor movement commands
    if (command.startsWith("M")) {
        motor_id = command.substring(1, 2).toInt(); // Extract motor ID
        angle = command.substring(2).toInt();       // Extract angle

        // Control the respective motor
        if (motor_id == 1) move_stepper(STEP1_PIN, DIR1_PIN, &current_steps[0], angle);
        else if (motor_id == 2) move_stepper(STEP2_PIN, DIR2_PIN, &current_steps[1], angle);
        else if (motor_id == 3) move_stepper(STEP3_PIN, DIR3_PIN, &current_steps[2], angle);
        else if (motor_id == 4) move_servo(servo1, angle);
        else if (motor_id == 5) move_servo(servo2, angle);
    }
}

// Arduino Setup Function
void setup() {
    // Initialize pin modes
    pinMode(STEP1_PIN, OUTPUT);
    pinMode(DIR1_PIN, OUTPUT);
    pinMode(STEP2_PIN, OUTPUT);
    pinMode(DIR2_PIN, OUTPUT);
    pinMode(STEP3_PIN, OUTPUT);
    pinMode(DIR3_PIN, OUTPUT);

    // Attach servos
    servo1.attach(SERVO1_PIN);
    servo2.attach(SERVO2_PIN);

    // Initialize UART
    Serial.begin(9600);
}

// Arduino Loop Function
void loop() {
    String command = "";

    // Read command from Serial until '\n'
    while (Serial.available() > 0) {
        char c = Serial.read();
        if (c == '\n') break; // End of command
        command += c;         // Append to command string
    }

    // Process the received command
    if (command.length() > 0) {
        process_command(command);
        delay(500); // Optional delay
    }
}

#include <reg51.h>
#include <stdlib.h>

// Pin Definitions
sbit SERVO1_PIN = P1^0;
sbit SERVO2_PIN = P1^1;
sbit STEP1_PIN = P1^2;
sbit DIR1_PIN = P1^3;
sbit STEP2_PIN = P1^4;
sbit DIR2_PIN = P1^5;
sbit STEP3_PIN = P1^6;
sbit DIR3_PIN = P1^7;

// Current Steps for Stepper Motors
int current_steps[3] = {0, 0, 0};

// UART Initialization
void UART_Init() {
    TMOD = 0x20;    // Timer1 in Mode 2 (8-bit auto-reload)
    TH1 = 0xFD;     // Baud rate 9600 for 11.0592 MHz crystal
    SCON = 0x50;    // Serial mode 1: 8-bit UART
    TR1 = 1;        // Start Timer1
}

// UART Receive Function
char UART_Rx() {
    while (!(RI));  // Wait for data
    RI = 0;         // Clear Receive Interrupt Flag
    return SBUF;    // Return Received Byte
}

// Delay Function
void delay(unsigned int time) {
    unsigned int i, j;
    for (i = 0; i < time; i++)
        for (j = 0; j < 1275; j++);
}
void process_command(char *command) {
    int motor_id, angle;
    if (command[0] == 'H' && command[1] == 'O' && command[2] == 'M' && command[3] == '\n') {
        move_servo(SERVO1_PIN, 90);
        move_servo(SERVO2_PIN, 90);
        move_stepper(STEP1_PIN, DIR1_PIN, &current_steps[0], 0);
        move_stepper(STEP2_PIN, DIR2_PIN, &current_steps[1], 0);
        move_stepper(STEP3_PIN, DIR3_PIN, &current_steps[2], 0);
        return;
    }

    if (command[0] == 'M') {
        motor_id = command[1] - '0'; // Extract Motor ID
        angle = atoi(&command[2]);   // Extract Angle

        if (motor_id == 1) move_stepper(STEP1_PIN, DIR1_PIN, &current_steps[0], angle);
        else if (motor_id == 2) move_stepper(STEP2_PIN, DIR2_PIN, &current_steps[1], angle);
        else if (motor_id == 3) move_stepper(STEP3_PIN, DIR3_PIN, &current_steps[2], angle);
        else if (motor_id == 4) move_servo(SERVO1_PIN, angle);
        else if (motor_id == 5) move_servo(SERVO2_PIN, angle);
    }
}


// Servo Motor Control
void move_servo(sbit SERVO_PIN, int angle) {
    unsigned int pulse_width = 1000 + ((angle * 1000) / 180); // Map 0-180° to 1-2 ms
    SERVO_PIN = 1;  
    delay(pulse_width / 100); // To Adjust for microcontroller timing
    SERVO_PIN = 0;  
    delay((20000 - pulse_width) / 100);  
}

// Stepper Motor Control
void move_stepper(sbit STEP_PIN, sbit DIR_PIN, int *current_steps, int target_angle) {
    int steps_per_revolution = 200;  //  1.8° step angle
    int target_steps = (target_angle % 360) * steps_per_revolution / 360;
    int step_difference = target_steps - *current_steps;

    if (step_difference > steps_per_revolution / 2)
        step_difference -= steps_per_revolution;
    else if (step_difference < -steps_per_revolution / 2)
        step_difference += steps_per_revolution;

    DIR_PIN = (step_difference > 0) ? 1 : 0;
    step_difference = abs(step_difference);

    for (int i = 0; i < step_difference; i++) {
        STEP_PIN = 1;
        delay(2); // we can Adjust  stepper speed
        STEP_PIN = 0;
        delay(2);
    }

    *current_steps = target_steps;
}

// Main Function
void main() {
  P1 = 0x00;  // Set Port 1 pins to low, configuring them as outputs.

    char command[10];
    UART_Init();

    while (1) {
        int i = 0;
        char c;

        while ((c = UART_Rx()) != '\n' && i < 9) { // Collect Command Until '\n'
            command[i++] = c;
        }
        command[i] = '\0';  // Null-Terminate String
        process_command(command); // Process Received Command
        delay(500); // Optional Delay
    }
}

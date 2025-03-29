#include <reg51.h>
#include <stdlib.h>

sbit SERVO1_PIN = P1^0;
sbit SERVO2_PIN = P1^1;
sbit STEP1_PIN = P1^2;
sbit DIR1_PIN = P1^3;
sbit STEP2_PIN = P1^4;
sbit DIR2_PIN = P1^5;
sbit STEP3_PIN = P1^6;
sbit DIR3_PIN = P1^7;

int current_steps[3] = {0, 0, 0};  // Current steps for stepper motors 1, 2, and 3

void UART_Init() {
    TMOD = 0x20;
    TH1 = 0xFD;
    SCON = 0x50;
    TR1 = 1;
}

char UART_Rx() {
    while (!(RI));  // Wait for the data to arrive
    RI = 0;         // Clear the receive interrupt flag
    return SBUF;    // Return the received byte
}

void delay(unsigned int time) {
    unsigned int i, j;
    for (i = 0; i < time; i++)
        for (j = 0; j < 1275; j++);
}

void move_servo(sbit SERVO_PIN, int angle) {
    unsigned int pulse_width = 1000 + ((angle * 1000) / 180);
    SERVO_PIN = 1;  
    delay(pulse_width);  
    SERVO_PIN = 0;  
    delay(20000 - pulse_width);  
}

void move_stepper(sbit STEP_PIN, sbit DIR_PIN, int *current_steps, int target_angle) {
    int steps_per_revolution = 200;  
    int target_steps, step_difference;

    target_angle = target_angle % 360;
    if (target_angle < 0) target_angle += 360;

    target_steps = (target_angle * steps_per_revolution) / 360;
    step_difference = target_steps - *current_steps;

    if (step_difference > steps_per_revolution / 2) {
        step_difference -= steps_per_revolution;
    } else if (step_difference < -steps_per_revolution / 2) {
        step_difference += steps_per_revolution;
    }

    if (step_difference > 0) {
        DIR_PIN = 1;
    } else {
        DIR_PIN = 0;
        step_difference = -step_difference;
    }

    for (int i = 0; i < step_difference; i++) {
        STEP_PIN = 1;  
        delay(2);      
        STEP_PIN = 0;  
        delay(2);      
    }

    *current_steps = target_steps;  
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
        motor_id = command[1] - '0';  
        angle = atoi(&command[2]);  

        if (motor_id == 1) {
            move_stepper(STEP1_PIN, DIR1_PIN, &current_steps[0], angle);
        } else if (motor_id == 2) {
            move_stepper(STEP2_PIN, DIR2_PIN, &current_steps[1], angle);
        } else if (motor_id == 3) {
            move_stepper(STEP3_PIN, DIR3_PIN, &current_steps[2], angle);
        } else if (motor_id == 4) {
            move_servo(SERVO1_PIN, angle);
        } else if (motor_id == 5) {
            move_servo(SERVO2_PIN, angle);
        }
    }
}

void main() {
    char command[10];
    UART_Init();

    while (1) {
        int i = 0;
        char c;
        while ((c = UART_Rx()) != '\n' && i < 9) {
            command[i++] = c;
        }
        command[i] = '\0'; 

        process_command(command);
        delay(500); 
    }
}

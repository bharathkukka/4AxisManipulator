import numpy as np

def forward_kinematics(theta1, theta2, theta3, theta4):
    # Link lengths from DH parameters
    L1 = 140  # Height from ground to base
    L2 = 25   # Length from base to second joint
    L3 = 250  # Length from second joint to third joint
    L4 = 150  # Length from third joint to end effector

    # Convert angles from degrees to radians
    theta1 = np.radians(theta1)
    theta2 = np.radians(theta2)
    theta3 = np.radians(theta3)
    theta4 = np.radians(theta4)

    # Calculate the transformation matrices for each joint
    T1 = np.array([[np.cos(theta1), -np.sin(theta1) * np.cos(0), np.sin(theta1) * np.sin(0), 0],
                   [np.sin(theta1), np.cos(theta1) * np.cos(0), -np.cos(theta1) * np.sin(0), 0],
                   [0, np.sin(0), np.cos(0), L1],
                   [0, 0, 0, 1]])

    T2 = np.array([[np.cos(theta2), -np.sin(theta2) * np.cos(np.pi/2), np.sin(theta2) * np.sin(np.pi/2), 0],
                   [np.sin(theta2), np.cos(theta2) * np.cos(np.pi/2), -np.cos(theta2) * np.sin(np.pi/2), 0],
                   [0, np.sin(np.pi/2), np.cos(np.pi/2), L2],
                   [0, 0, 0, 1]])

    T3 = np.array([[np.cos(theta3), -np.sin(theta3) * np.cos(0), np.sin(theta3) * np.sin(0), L3 * np.cos(theta3)],
                   [np.sin(theta3), np.cos(theta3) * np.cos(0), -np.cos(theta3) * np.sin(0), L3 * np.sin(theta3)],
                   [0, np.sin(0), np.cos(0), 0],
                   [0, 0, 0, 1]])

    T4 = np.array([[np.cos(theta4), -np.sin(theta4) * np.cos(np.pi/2), np.sin(theta4) * np.sin(np.pi/2), 0],
                   [np.sin(theta4), np.cos(theta4) * np.cos(np.pi/2), -np.cos(theta4) * np.sin(np.pi/2), 0],
                   [0, np.sin(np.pi/2), np.cos(np.pi/2), L4],
                   [0, 0, 0, 1]])

    # Calculate the overall transformation matrix
    T_total = T1 @ T2 @ T3 @ T4

    # Extract the position of the end effector
    x = T_total[0, 3]
    y = T_total[1, 3]
    z = T_total[2, 3]

    return x, y, z

# Example usage for Home Position
home_position_angles = [90, 90, 90, 90]  # Degrees
x_home, y_home, z_home = forward_kinematics(*home_position_angles)
print(f"Home Position: x={x_home}, y={y_home}, z={z_home}")


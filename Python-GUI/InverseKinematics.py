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

import numpy as np

def inverse_kinematics(x, y, z):
    # Define link lengths based on DH parameters
    L1 = 140  # Vertical height to base
    L2 = 25   # Distance to joint 2
    L3 = 250  # Distance to joint 3
    L4 = 150  # Length to end effector from joint 4

    # Calculate theta1 (base joint)
    theta1 = np.arctan2(y, x)
    print(f"θ1 (theta1) = {np.degrees(theta1):.2f}°")

    # Horizontal distance from base to target (r)
    r = np.sqrt(x ** 2 + y ** 2)

    # Adjusted vertical reach distance to target
    z_reach = z - L1  # Remove base height from calculation

    # Total reach distance to target in 3D space
    reach = np.sqrt(r ** 2 + z_reach ** 2)

    # Calculate theta3 based on reach distance
    cos_theta3 = (reach ** 2 - L2 ** 2 - L3 ** 2) / (2 * L2 * L3)
    theta3 = np.arccos(np.clip(cos_theta3, -1, 1))  # Clip to valid range
    print(f"θ3 (theta3) = {np.degrees(theta3):.2f}°")

    # Calculate theta2 using triangle formed with L2 and L3
    k1 = L2 + L3 * np.cos(theta3)
    k2 = L3 * np.sin(theta3)
    theta2 = np.arctan2(z_reach, r) - np.arctan2(k2, k1)
    print(f"θ2 (theta2) = {np.degrees(theta2):.2f}°")

    # θ4 - To align end-effector horizontally (assuming no twist for simplicity)
    theta4 = 0
    print(f"θ4 (theta4) = {theta4:.2f}°")

    return np.degrees(theta1), np.degrees(theta2), np.degrees(theta3), theta4

# Example usage
x_target, y_target, z_target = 0, 150, 415  # Desired position (home position)
theta1, theta2, theta3, theta4 = inverse_kinematics(x_target, y_target, z_target)
print(f"Joint angles: θ1={theta1}, θ2={theta2}, θ3={theta3}, θ4={theta4}")

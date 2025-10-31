import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define DH parameters
l1 = 140  # Length of the first link (height)
l2 = 25   # Length of the second link
l3 = 250  # Length of the third link
l4 = 150  # Length of the fourth link (gripper)

# Forward Kinematics Function
def forward_kinematics(theta1, theta2, theta3, theta4):
    # Homogeneous transformation matrices based on DH parameters
    T1 = np.array([[np.cos(theta1), -np.sin(theta1), 0, l1 * np.cos(theta1)],
                   [np.sin(theta1), np.cos(theta1), 0, l1 * np.sin(theta1)],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    T2 = np.array([[np.cos(theta2), -np.sin(theta2), 0, l2 * np.cos(theta2)],
                   [0, 0, -1, 0],
                   [np.sin(theta2), np.cos(theta2), 0, l2 * np.sin(theta2)],
                   [0, 0, 0, 1]])

    T3 = np.array([[np.cos(theta3), -np.sin(theta3), 0, l3 * np.cos(theta3)],
                   [0, 0, -1, 0],
                   [np.sin(theta3), np.cos(theta3), 0, l3 * np.sin(theta3)],
                   [0, 0, 0, 1]])

    T4 = np.array([[np.cos(theta4), -np.sin(theta4), 0, l4 * np.cos(theta4)],
                   [0, 0, -1, 0],
                   [np.sin(theta4), np.cos(theta4), 0, l4 * np.sin(theta4)],
                   [0, 0, 0, 1]])

    # Calculate the combined transformation
    T = T1 @ T2 @ T3 @ T4  # Multiply transformation matrices
    x = T[0, 3]  # Extract position
    y = T[1, 3]
    z = T[2, 3]
    return x, y, z

# Define the inverse kinematics function (to be implemented)
def inverse_kinematics(x, y, z):
    # Placeholder for inverse kinematics calculations
    # Return theta1, theta2, theta3, theta4 based on x, y, z
    # You need to implement this based on your robot's kinematic equations
    return np.radians(90), np.radians(0), np.radians(0), np.radians(90)  # Example values

# Create a list to store points in the workspace
points = []

# Define the joint ranges
theta1_range = np.linspace(0, 2 * np.pi, 10)  # 0 to 360 degrees
theta2_range = np.linspace(0, 2 * np.pi, 10)  # 0 to 360 degrees
theta3_range = np.linspace(0, 2 * np.pi, 10)  # 0 to 360 degrees
theta4_range = np.linspace(0, np.pi, 10)  # 0 to 180 degrees

# Calculate points in the workspace
for theta1 in theta1_range:
    for theta2 in theta2_range:
        for theta3 in theta3_range:
            for theta4 in theta4_range:
                x, y, z = forward_kinematics(theta1, theta2, theta3, theta4)
                points.append((x, y, z))

# Convert points to a NumPy array for easier indexing
points = np.array(points)

# Visualize the workspace
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(points[:, 0], points[:, 1], points[:, 2], alpha=0.1)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
plt.title("Robot Workspace")
plt.show()

# Example Pick-and-Place Coordinates
X_pick, Y_pick, Z_pick = 50, 50, 0  # Example pick coordinates
X_place, Y_place, Z_place = 100, 100, 0  # Example place coordinates

# Calculate the inverse kinematics for the pick position
theta1_pick, theta2_pick, theta3_pick, theta4_pick = inverse_kinematics(X_pick, Y_pick, Z_pick)

# Output the joint angles for the pick position
print(f"Joint angles for pick position: θ1: {np.degrees(theta1_pick):.2f}, θ2: {np.degrees(theta2_pick):.2f}, θ3: {np.degrees(theta3_pick):.2f}, θ4: {np.degrees(theta4_pick):.2f}")

# Calculate the inverse kinematics for the place position
theta1_place, theta2_place, theta3_place, theta4_place = inverse_kinematics(X_place, Y_place, Z_place)

# Output the joint angles for the place position
print(f"Joint angles for place position: θ1: {np.degrees(theta1_place):.2f}, θ2: {np.degrees(theta2_place):.2f}, θ3: {np.degrees(theta3_place):.2f}, θ4: {np.degrees(theta4_place):.2f}")

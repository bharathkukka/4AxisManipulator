# Serial communication
# pip install pyserial for serial communication between PC and micro8051
import tkinter as tk
from tkinter import messagebox
import serial
import time
from PIL import Image, ImageTk

# InitializATION OF Serial Communication
try:
    ser = serial.Serial('/dev/tty.usbserial-1130', 9600)
    time.sleep(2)  # Allow time for connection to establish
except serial.SerialException:
    ser = None
    messagebox.showerror("Error", "Could not open serial port")


# Function to send motor angle data to 8051
def send_motor_command(motor_id, angle):
    if ser:
        command = f"M{motor_id}{angle:03d}\n"
        ser.write(command.encode())
    else:
        print(f"Motor {motor_id} angle set to {angle}° (No serial connection)")


# Function for sliders
def update_angle(motor_id, angle):
    send_motor_command(motor_id, int(angle))


# Home Position Button Function
def set_home_position():
    home_positions = [0, 0, 0, 90, 90]  # Define home positions for all motors
    print("Setting home positions:")
    for i, slider in enumerate(sliders):
        slider.set(home_positions[i])  # Reset each slider to its home position
        update_angle(i + 1, home_positions[i])  # Send home position command to motors
        print(f"Motor {i + 1}: {home_positions[i]}°")  # Debugging output

    if ser:
        ser.write(b"HOM\n")  # Send home command to the robotic arm
    root.update()  # Update the GUI to reflect changes


# Functions to record and execute gestures
gestures = {}


def record_gesture(gesture_id):
    angles = [int(slider.get()) for slider in sliders]
    gestures[gesture_id] = angles
    messagebox.showinfo("Gesture Saved", f"Gesture {gesture_id} saved with angles {angles}")


def play_gesture(gesture_id):
    if gesture_id in gestures:
        for i, angle in enumerate(gestures[gesture_id]):
            send_motor_command(i + 1, angle)
            time.sleep(0.5)
    else:
        messagebox.showerror("Error", f"Gesture {gesture_id} not found")


# Setup UI
root = tk.Tk()
root.title("5DOF Robotic Arm Control")
root.attributes("-fullscreen", True)  # Fullscreen mode

# Load and set up the background image
bg_image = Image.open("/Users/bharathgoud/PycharmProjects/Robotics/Robotics/5DOF/GUI/Gemini_Generated_Image_jjcceojjcceojjcc.jpg")  # Use your image path here
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Set font style for buttons and labels
font_style = ("Times New Roman", 14, "bold")

# Calculate initial placement coordinates to center all elements
base_x = screen_width // 2 - 200  # Centralize horizontally
base_y = screen_height // 2 - 200  # Centralize vertically

# Project Title
title_label = tk.Label(root, text="5DOF Pick&Place Robotic ARM", font=("Times New Roman", 30, "bold"),
                        fg="red")  # Removed bg parameter
title_label.place(relx=0.5, y=76, anchor='center')  # Centered horizontally, 76 pixels from the top

# Define motor names for all motors
motor_names = ["BASE", "SHOULDER", "ELBOW", "WRIST", "GRIPPER"]
# Sliders for motor angles
sliders = []
angle_labels = []  # List to hold labels for angle values
for i in range(5):
    # Use motor_names list to set the label text
    label = tk.Label(root, text=f"{motor_names[i]} POSITION", font=font_style, bg="white", fg="black")
    label.place(x=base_x, y=base_y + i * 60)

    if i < 3:  # For the first three motors (stepper motors)
        slider = tk.Scale(root, from_=-360, to=360, orient=tk.HORIZONTAL, length=300, font=font_style,
                          command=lambda angle, i=i: update_angle(i + 1, angle), bg="grey", troughcolor="darkred",resolution=45)
        slider.set(0)  # Set initial position to home (90°)
    else:  # For the last two motors (servo motors)
        slider = tk.Scale(root, from_=0, to=180, orient=tk.HORIZONTAL, length=300, font=font_style,
                          command=lambda angle, i=i: update_angle(i + 1, angle), bg="grey", troughcolor="darkred",resolution=45)
        slider.set(90)  # Set initial position to home (90°)

    slider.place(x=base_x + 200, y=base_y + i * 60)
    sliders.append(slider)

    # Create a label to display the angle value
    angle_label = tk.Label(root, text=f"{slider.get()}°", font=font_style, bg="white", fg="black")
    angle_label.place(x=base_x + 520, y=base_y + i * 60)  # Position the label next to the slider
    angle_labels.append(angle_label)

    # Update the angle label when the slider is moved
    def update_angle_label(value, index=i):
        angle_labels[index].config(text=f"{value}°")

    slider.config(command=lambda angle, i=i: (update_angle(i + 1, angle), update_angle_label(angle, i)))


# Define gesture names
gesture_names = ["PICK", "PLACE", "GESTURE"]

# Home Position Button
home_button = tk.Button(root, text="HOME POSITION", command=set_home_position,
                        bg="lightblue", fg="black", font=font_style, width=20, height=2)
home_button.place(x=(screen_width // 2 - 150) + 100, y=base_y + 5 * 60 + 25)

# Gesture Buttons
for j in range(3):  # Adjusted to loop through the length of gesture_names
    record_button = tk.Button(root, text=f" RECORD:{gesture_names[j]}",
                              command=lambda j=j: record_gesture(j + 1),
                              bg="lightgreen", fg="black", font=font_style, width=20, height=2)

    play_button = tk.Button(root, text=f"PLAY: {gesture_names[j]}",
                            command=lambda j=j: play_gesture(j + 1),
                            bg="orange", fg="black", font=font_style, width=20, height=2)

    # Place buttons for gestures
    record_button.place(x=base_x, y=base_y + 5 * 60 + 80 + (j) * 60)
    play_button.place(x=base_x + 300, y=base_y + 5 * 60 + 80 + (j) * 60)

# Global variable to track the selected slider
selected_slider = None

# Function to set the currently selected slider
def set_selected_slider(index):
    global selected_slider
    selected_slider = index

# Key bindings for controlling the currently selected motor with keyboard
def increase_selected_angle():
    if selected_slider is not None:
        current_value = sliders[selected_slider].get()
        new_value = min(current_value + 45, sliders[selected_slider]['to'])  # Limit to max angle
        sliders[selected_slider].set(new_value)  # Update slider position
        update_angle(selected_slider + 45, new_value)  # Send updated angle to the motor
        print(f"Increased motor {selected_slider + 45} to {new_value}°")  # Debugging output
    else:
        print("No motor selected.")

def decrease_selected_angle():
    if selected_slider is not None:
        current_value = sliders[selected_slider].get()
        new_value = max(current_value - 45, sliders[selected_slider]['from'])  # Limit to min angle
        sliders[selected_slider].set(new_value)  # Update slider position
        update_angle(selected_slider + 45, new_value)  # Send updated angle to the motor
        print(f"Decreased motor {selected_slider + 45} to {new_value}°")  # Debugging output
    else:
        print("No motor selected.")


# Function to handle slider click events to set the selected slider
def on_slider_click(index):
    set_selected_slider(index)

# Binding mouse click events to sliders
for i, slider in enumerate(sliders):
    slider.bind("<Button-1>", lambda event, index=i: on_slider_click(index))

# Key bindings for controlling the currently selected motor with keyboard
root.bind('<Left>', lambda event: decrease_selected_angle())  # Left arrow decreases angle
root.bind('<Right>', lambda event: increase_selected_angle())  # Right arrow increases angle

root.mainloop()

#ls /dev/tty.* for checking the port and
# screen /dev/tty.usbserial-XXXX 9600  to Verify Communication (Optional):


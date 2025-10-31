import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time
from PIL import Image, ImageTk


# Class for Serial Communication
class SerialHandler:
    def __init__(self, port, baud_rate):
        self.ser = None
        try:
            self.ser = serial.Serial(port, baud_rate)
            time.sleep(2)  # Allow time for connection to establish
        except serial.SerialException:
            self.ser = None
            messagebox.showerror("Error", "Could not open serial port")

    def send_command(self, command):
        if self.ser:
            try:
                self.ser.write(command.encode())
            except serial.SerialException:
                messagebox.showerror("Error", "Failed to send data to serial port")
        else:
            print("No serial connection. Command not sent:", command)

    def close(self):
        if self.ser:
            self.ser.close()


# Class for the Robotic Arm Control
class RoboticArmControl:
    def __init__(self, root, serial_handler):
        self.root = root
        self.serial_handler = serial_handler
        self.sliders = []
        self.angle_labels = []
        self.gestures = {}
        self.selected_slider = None
        self.home_positions = [90, 90, 90, 90, 90]

        # Initialize UI
        self.setup_ui()

    def setup_ui(self):
        # Fullscreen Window Setup
        self.root.title("5DOF Robotic Arm Control")
        self.root.attributes("-fullscreen", True)

        # Load and set up the background image
        bg_image = Image.open("/Robotics/5DOF/GUI/Gemini_Generated_Image_jjcceojjcceojjcc.jpg")  # Update with your image path
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)

        canvas = tk.Canvas(self.root, width=screen_width, height=screen_height)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor="nw", image=bg_photo)

        # Font Style
        font_style = ("Times New Roman", 14, "bold")

        # Project Title
        title_label = tk.Label(self.root, text="5DOF Pick&Place Robotic ARM", font=("Times New Roman", 30, "bold"), fg="red")
        title_label.place(relx=0.5, y=76, anchor='center')

        # Motor Sliders and Labels
        motor_names = ["BASE", "SHOULDER", "ELBOW", "WRIST", "GRIPPER"]
        base_x = screen_width // 2 - 200
        base_y = screen_height // 2 - 200

        for i in range(5):
            label = tk.Label(self.root, text=f"{motor_names[i]} POSITION", font=font_style, bg="white", fg="black")
            label.place(x=base_x, y=base_y + i * 60)

            if i < 3:
                slider = tk.Scale(self.root, from_=-240, to=450, orient=tk.HORIZONTAL, length=300, font=font_style,
                                  bg="grey", troughcolor="darkred", command=lambda angle, i=i: self.update_angle(i + 1, angle))
            else:
                slider = tk.Scale(self.root, from_=0, to=180, orient=tk.HORIZONTAL, length=300, font=font_style,
                                  bg="grey", troughcolor="darkred", command=lambda angle, i=i: self.update_angle(i + 1, angle))

            slider.set(90)
            slider.place(x=base_x + 200, y=base_y + i * 60)
            self.sliders.append(slider)

            angle_label = tk.Label(self.root, text=f"{slider.get()}°", font=font_style, bg="white", fg="black")
            angle_label.place(x=base_x + 520, y=base_y + i * 60)
            self.angle_labels.append(angle_label)

            slider.bind("<Button-1>", lambda event, index=i: self.set_selected_slider(index))

        # Home Position Button
        home_button = tk.Button(self.root, text="HOME POSITION", command=self.set_home_position,
                                bg="lightblue", fg="black", font=font_style, width=20, height=2)
        home_button.place(x=(screen_width // 2 - 150) + 100, y=base_y + 5 * 60 + 25)

        # Gesture Buttons
        gesture_names = ["PICK", "PLACE", "GESTURE"]
        for j, gesture_name in enumerate(gesture_names):
            record_button = tk.Button(self.root, text=f"RECORD: {gesture_name}",
                                      command=lambda j=j: self.record_gesture(j + 1),
                                      bg="lightgreen", fg="black", font=font_style, width=20, height=2)
            play_button = tk.Button(self.root, text=f"PLAY: {gesture_name}",
                                    command=lambda j=j: self.play_gesture(j + 1),
                                    bg="orange", fg="black", font=font_style, width=20, height=2)
            record_button.place(x=base_x, y=base_y + 5 * 60 + 80 + j * 60)
            play_button.place(x=base_x + 300, y=base_y + 5 * 60 + 80 + j * 60)

        # Key Bindings for Motor Control
        self.root.bind('<Left>', lambda event: self.decrease_selected_angle())
        self.root.bind('<Right>', lambda event: self.increase_selected_angle())

    def set_selected_slider(self, index):
        self.selected_slider = index

    def update_angle(self, motor_id, angle):
        self.serial_handler.send_command(f"M{motor_id}{int(angle):03d}\n")
        self.angle_labels[motor_id - 1].config(text=f"{angle}°")

    def set_home_position(self):
        for i, slider in enumerate(self.sliders):
            slider.set(self.home_positions[i])
            self.update_angle(i + 1, self.home_positions[i])
        self.serial_handler.send_command("HOM\n")

    def record_gesture(self, gesture_id):
        angles = [int(slider.get()) for slider in self.sliders]
        self.gestures[gesture_id] = angles
        messagebox.showinfo("Gesture Saved", f"Gesture {gesture_id} saved with angles {angles}")

    def play_gesture(self, gesture_id):
        if gesture_id in self.gestures:
            angles = self.gestures[gesture_id]
            threading.Thread(target=self.execute_gesture, args=(angles,)).start()
        else:
            messagebox.showerror("Error", f"Gesture {gesture_id} not found")

    def execute_gesture(self, angles):
        for i, angle in enumerate(angles):
            self.update_angle(i + 1, angle)
            time.sleep(0.5)

    def increase_selected_angle(self):
        if self.selected_slider is not None:
            current_value = self.sliders[self.selected_slider].get()
            new_value = min(current_value + 1, self.sliders[self.selected_slider]['to'])
            self.sliders[self.selected_slider].set(new_value)
            self.update_angle(self.selected_slider + 1, new_value)

    def decrease_selected_angle(self):
        if self.selected_slider is not None:
            current_value = self.sliders[self.selected_slider].get()
            new_value = max(current_value - 1, self.sliders[self.selected_slider]['from'])
            self.sliders[self.selected_slider].set(new_value)
            self.update_angle(self.selected_slider + 1, new_value)


# Main Execution
if __name__ == "__main__":
    port = "/dev/ttyUSB0"  # Update with your port
    baud_rate = 9600

    root = tk.Tk()
    serial_handler = SerialHandler(port, baud_rate)
    app = RoboticArmControl(root, serial_handler)
    root.mainloop()

    # Close serial connection on exit
    serial_handler.close()

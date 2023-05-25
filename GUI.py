import tkinter as tk
from tkinter import messagebox
import math
import copy
import threading
from main import perform_simulation
from send_arr import send_array

class FractalDrawer:
    def __init__(self, master):
        self.master = master
        self.master.title("Fractal Drawer")

        # Set up canvas for drawing path
        self.canvas = tk.Canvas(self.master, bg="black", width=600, height=400, highlightthickness=0)
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)
        self.canvas.bind("<B1-Motion>", self.track_path)
        self.canvas.bind("<ButtonPress-1>", self.start_sampling)  # Bind mouse button press event
        self.canvas.bind("<ButtonRelease-1>", self.stop_sampling)  # Bind mouse button release event
        self.line_color = "yellow"

        # Set up angle slider and input box
        self.angle_var = tk.DoubleVar()
        self.angle_var.set(0.0)
        self.angle_slider = tk.Scale(self.master, label="Angle (degrees)", from_=0, to=360, variable=self.angle_var,
                                     orient=tk.HORIZONTAL, command=self.update_angle)
        self.angle_slider.pack(side=tk.TOP, padx=10, pady=10)
        self.angle_input = tk.Entry(self.master, textvariable=self.angle_var)
        self.angle_input.pack(side=tk.TOP, padx=10, pady=5)

        # Set up iteration count slider and input box
        self.iteration_var = tk.IntVar()
        self.iteration_var.set(1)
        self.iteration_slider = tk.Scale(self.master, label="Iteration Count", from_=1, to=10000, variable=self.iteration_var,
                                     orient=tk.HORIZONTAL, command=self.update_iteration)
        self.iteration_slider.pack(side=tk.TOP, padx=10, pady=10)
        self.iteration_input = tk.Entry(self.master, textvariable=self.iteration_var)
        self.iteration_input.pack(side=tk.TOP, padx=10, pady=5)
        self.iteration_input.bind("<FocusOut>", self.update_iteration_input)  # Bind focus out event to update iteration slider

        # Set up send path button
        self.send_button = tk.Button(self.master, text="Send the path", command=self.show_popup)
        self.send_button.pack(side=tk.TOP, padx=10, pady=10)

        # Set up print path button
        self.print_button = tk.Button(self.master, text="Print Path", command=self.print_path)
        self.print_button.pack(side=tk.TOP, padx=10, pady=10)

        # Set up simulation button
        self.simulation_button = tk.Button(self.master, text="Perform Simulation", command=self.simulate)
        self.simulation_button.pack(side=tk.TOP, padx=(5, 10), pady=10)

        # Set up clear button
        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        # List to store path coordinates
        self.sampling_active = False
        self.path = []
        self.sample_interval = 40  # Sample interval in milliseconds
        self.count = 0

        #Timer
        self.timer = None

        #Corner Cutting Parameters
        self.max_deviation = 30
        self.max_iteration = 40

    def track_path(self, event):
        # Start the timer if it's not already running
        if not self.timer:
            self.timer = threading.Timer(0.05, self.append_point)
            self.timer.start()

    def stop_sampling(self, event):
        if self.timer:
            self.timer.cancel()  # Stop the timer
            self.timer = None
    
    def simulate(self):
        perform_simulation(self.path)

    def append_point(self):
        # Append the current mouse coordinates to the path
        if self.timer:
            x, y = self.canvas.winfo_pointerxy()
            x -= self.canvas.winfo_rootx()
            y -= self.canvas.winfo_rooty()
            self.path.append((x, y))

            self.count += 1
            print("New point " + str(self.count))
            if len(self.path) > 1:
                prev_x, prev_y = self.path[-2]
                self.canvas.create_line(prev_x, prev_y, x, y, width=3, smooth=True , fill=self.line_color)

        # Restart the timer for the next interval
        self.timer = threading.Timer(0.05, self.append_point)
        self.timer.start()

    def show_popup(self):
        # Show a popup information window with the message "Path is sent!"
        send_array()
        messagebox.showinfo("Information", "Path is sent!")

    def print_path(self):
        # Print the path coordinates to console
        print("Path coordinates:" + " (Length: " + str(len(self.path)) + ")")
        for point in self.path:
            print("({}, {})".format(point[0], point[1]))

    def clear_canvas(self):
        # Clear the canvas and reset the path list
        self.canvas.delete("all")
        self.path = []

    def update_angle(self, angle):
        # Update angle variable from slider and input box
        self.angle_var.set(float(angle))
        self.angle_input.delete(0, tk.END)
        self.angle_input.insert(tk.END, angle)

    def update_iteration(self, iteration):
        # Update iteration count variable from slider and input box
        self.iteration_var.set(int(iteration))
        self.iteration_input.delete(0, tk.END)
        self.iteration_input.insert(tk.END, iteration)

    def update_angle_input(self, event):
    # Update angle slider value based on input box change
        try:
            value = float(self.angle_var.get())
            self.angle_slider.set(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
    def update_iteration_input(self, event):
        # Update iteration count slider value based on input box change
        try:
            value = int(self.iteration_var.get())
            self.iteration_slider.set(value)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")

    def start_sampling(self, event):
        # Start the sampling when the mouse button is pressed
        if not self.timer:
            self.timer = threading.Timer(0.05, self.append_point)
            self.timer.start()

    def stop_sampling(self, event):
        if self.timer:
            self.timer.cancel()  # Stop the timer
            self.timer = None

            self.remove_duplicates()
            self.corner_cut()
            self.visualize_path()

    def remove_duplicates(self):
        # Remove duplicate points from the path list
        counts = {}
        for point in self.path:
            counts[point] = counts.get(point, 0) + 1
        self.path = [point for point in self.path if counts[point] < 5]

    def corner_cut(self):
        for i in range(self.max_iteration):
            entered = False
            temp = [self.path[0]]
            for i in range(1, len(self.path) - 1):
                angle1_rad = math.atan2((self.path[i][1] - self.path[i - 1][1]), (self.path[i][0] - self.path[i - 1][0]))
                angle2_rad = math.atan2((self.path[i + 1][1] - self.path[i][1]), (self.path[i + 1][0] - self.path[i][0]))
                diff = math.atan2((math.cos(angle1_rad) * math.sin(angle2_rad) - math.cos(angle2_rad) * math.sin(angle1_rad)),
                                (math.sin(angle1_rad) * math.sin(angle2_rad) + math.cos(angle1_rad) * math.cos(angle2_rad)))

                while diff > math.pi:
                    diff -= 2 * math.pi
                while diff < -math.pi:
                    diff += 2 * math.pi

                if abs(diff) * 180 / math.pi > self.max_deviation:
                    entered = True
                    new_x = (self.path[i - 1][0] + self.path[i + 1][0]) / 2
                    new_y = (self.path[i - 1][1] + self.path[i + 1][1]) / 2
                    new_data = (int(new_x), int(new_y))
                    temp.append(new_data)
                else:
                    temp.append(self.path[i])
            
            if not entered:
                break
            
            temp.append(self.path[-1])
            self.path = temp

    def visualize_path(self):
        # Create a new window for visualization
        visual_window = tk.Toplevel(self.master)
        visual_window.title("Path Visualization")

        # Set up canvas for drawing the path
        visual_canvas = tk.Canvas(visual_window, bg="black", width=600, height=400, highlightthickness=0)
        visual_canvas.pack(side=tk.TOP, padx=10, pady=10)

        # Draw the path on the canvas using the same colors
        if len(self.path) > 1:
            prev_x, prev_y = self.path[0]
            for i in range(1, len(self.path)):
                x, y = self.path[i]
                visual_canvas.create_line(prev_x, prev_y, x, y, width=3, smooth=True, fill=self.line_color)
                prev_x, prev_y = x, y

    def compare_lists(self,list1,list2):
        if len(list1) != len(list2):
            return False

        for item1, item2 in zip(list1, list2):
            if item1 != item2:
                return False

        return True


root = tk.Tk()
app = FractalDrawer(root)
root.mainloop()

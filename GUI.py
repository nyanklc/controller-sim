import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import math
import copy
import threading
from main import perform_simulation
from send_arr import send_array
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from car import getDistance

class FractalDrawer:
    def __init__(self, master):

        self.master = master
        self.master.title("Path Drawing")

        self.sidebar_frame = ctk.CTkFrame(self.master, width=650, height=450, corner_radius=7)
        self.sidebar_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.sidebar_frame2 = ctk.CTkFrame(self.master, width=650, height=450, corner_radius=7)
        self.sidebar_frame2.pack(side=tk.RIGHT, padx=10, pady=10)

        self.sidebar_frame3 = ctk.CTkFrame(self.master, width=500, height=500, corner_radius=7)
        self.sidebar_frame3.pack(side=tk.RIGHT, padx=10, pady=10)

        # yazı
        self.label = ctk.CTkLabel(self.sidebar_frame3, text="Actual Path to be Sent", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(side=tk.TOP, padx=20, pady=(2,2))

        # yazı
        self.label = ctk.CTkLabel(self.sidebar_frame, text="Drawing Canvas", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(side=tk.TOP, padx=20, pady=(2,2))

        # Set up canvas for drawing path
        self.canvas = ctk.CTkCanvas(self.sidebar_frame, bg="white", width=650, height=450, highlightthickness=0)
        self.canvas.pack(side=tk.TOP, padx=10, pady=(2,2))
        self.canvas.bind("<B1-Motion>", self.track_path)
        self.canvas.bind("<ButtonPress-1>", self.start_sampling)  # Bind mouse button press event
        self.canvas.bind("<ButtonRelease-1>", self.stop_sampling)  # Bind mouse button release event
        self.line_color = "blue"

        # yazı
        self.vis_label = ctk.CTkLabel(self.sidebar_frame, text="Smoothed Path", font=ctk.CTkFont(size=16, weight="bold"))
        self.vis_label.pack(side=tk.TOP, padx=10, pady=(2,2))

        # Set up canvas for drawing the path
        self.visual_canvas = ctk.CTkCanvas(self.sidebar_frame, bg="white", width=650, height=450, highlightthickness=0)
        self.visual_canvas.pack(side=tk.BOTTOM, padx=10, pady=(2,10))

        v = tk.StringVar()
        v.set(2)

        # yazı
        self.vis_label = ctk.CTkLabel(self.sidebar_frame2, text="Corner Smoothing Degree", font=ctk.CTkFont(size=14))
        self.vis_label.pack(side=tk.TOP, padx=10, pady=(2,2))

        ctk.CTkRadioButton(self.sidebar_frame2, text="Low", variable=v, value=1).pack(pady=(10,0))
        ctk.CTkRadioButton(self.sidebar_frame2, text="Medium", variable=v, value=2).pack()
        ctk.CTkRadioButton(self.sidebar_frame2, text="High", variable=v, value=3).pack()

        # Set up send path button
        self.send_button = ctk.CTkButton(self.sidebar_frame2, text="Send the path", command=self.show_popup)
        self.send_button.pack(side=tk.TOP, padx=10, pady=(60,10))

        # Set up print path button
        self.print_button = ctk.CTkButton(self.sidebar_frame2, text="Print Path", command=self.print_path)
        self.print_button.pack(side=tk.TOP, padx=10, pady=10)

        # Set up simulation button
        self.simulation_button = ctk.CTkButton(self.sidebar_frame2, text="Perform Simulation", command=self.simulate)
        self.simulation_button.pack(side=tk.TOP, padx=(10, 10), pady=10)

        # Set up clear button
        self.clear_button = ctk.CTkButton(self.sidebar_frame2, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.TOP, padx=10, pady=10)


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

        self.pltcanvas = None

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
        self.sidebar_frame3.destroy()
        self.sidebar_frame3 = ctk.CTkFrame(self.master, width=500, height=500, corner_radius=7)
        self.sidebar_frame3.pack(side=tk.RIGHT, padx=10, pady=10)
        # yazı
        self.label = ctk.CTkLabel(self.sidebar_frame3, text="Actual Path to be Sent (in meters)", font=ctk.CTkFont(size=16, weight="bold"))
        self.label.pack(side=tk.TOP, padx=20, pady=(2,2))
        perform_simulation(self.path)
        # the figure that will contain the plot
        fig = Figure(figsize = (5, 5), dpi = 100)
        # adding the subplot
        plot1 = fig.add_subplot(111)
        x = np.load("./pos_arr_x.npy")*0.005
        y = np.load("./pos_arr_y.npy")*0.005
        plot1.plot(x, -y, "-gD")
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.pltcanvas = FigureCanvasTkAgg(fig, master = self.sidebar_frame3)
        self.pltcanvas.draw()
        # placing the canvas on the Tkinter window
        self.pltcanvas.get_tk_widget().pack()   
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.pltcanvas, self.sidebar_frame3)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        self.pltcanvas.get_tk_widget().pack()

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
        messagebox.showinfo("Information", "Path is completely sent!")
        

    def print_path(self):
        # Print the path coordinates to console
        print("Path coordinates:" + " (Length: " + str(len(self.path)) + ")")
        for point in self.path:
            print("({}, {})".format(point[0], point[1]))

    def clear_canvas(self):
        # Clear the canvas and reset the path list
        self.visual_canvas.delete("all")
        self.canvas.delete("all")
        if self.pltcanvas:
            for item in self.pltcanvas.get_tk_widget().find_all():
                self.pltcanvas.get_tk_widget().delete(item)
            self.pltcanvas = None
        self.path.clear()

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
            self.dilute()
            self.corner_cut()
            self.dilute()
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

    def dilute(self):
        for i in range(10):
            temp = [self.path[0]]
            i = 1
            adjusted = False
            while i + 1 < len(self.path):
                distance = getDistance(self.path[i], self.path[i-1])
                if distance < 5:
                    adjusted = True
                    temp.append(self.path[i+1])
                    i += 2
                else:
                    temp.append(self.path[i])
                    i += 1
            
            if not adjusted:
                break

            temp.append(self.path[-1])
            self.path = temp

    def visualize_path(self):
        
        visual_canvas = self.visual_canvas
        
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

ctk.set_appearance_mode("light")
root = ctk.CTk()
app = FractalDrawer(root)
root.mainloop()

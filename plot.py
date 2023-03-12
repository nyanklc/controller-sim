import math
import time

import matplotlib as mpl
# mpl.use('Agg')
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pygame
import numpy as np

from car import Car
from game_window import GameWindow

######################################################################
sim_end_time = 10.0

p = 0.4
i = 0.04
d = 0.00001

goal = 100.0

# NOTE: need to reduce derivative gain when making the time step smaller, otherwise it becomes unstable
time_step = 0.001

finish_enabled = False
finish_error = 2
finish_derivative_error = 0.01

viewer_size = (640, 480)
######################################################################

def finished(speeds, goal, time_index):
    if (not finish_enabled):
        return False
    # basically checking if value is in the error range, AND if its derivative is close to zero
    if len(speeds) == 0:
        return False
    if time_index < 2:
        return False

    asd = speeds[time_index - 1]
    err = math.fabs(asd - goal)
    if err < finish_error:
        diff = asd - speeds[time_index - 2]
        if math.fabs(diff) < finish_derivative_error:
            return True
    return False

def clip_plots(time_index, plot_time, plot_last_error, plot_goal, plot_vel):
    a = plot_time[:time_index-1]
    b = plot_last_error[:time_index-1]
    c = plot_goal[:time_index-1]
    d = plot_vel[:time_index-1]
    return (a, b, c, d)

if __name__ == "__main__":
    car = Car(color=(255, 0, 255), x=200, y=100, yaw=math.pi/6)

    pid_params = (p, i, d, goal) # assuming car starts with 0 velocity, otherwise also set last_measurement param
    car.setController('pid', pid_params)
    car.setAngularController('pid', pid_params)
    car.setSpeed(goal)

    print("starting simulation")

    plot_time = np.zeros(shape=(int)(sim_end_time/time_step) + 1, dtype=np.float32)
    plot_last_error = np.zeros(shape=(int)(sim_end_time/time_step) + 1, dtype=np.float32)
    plot_goal = np.zeros(shape=(int)(sim_end_time/time_step) + 1, dtype=np.float32)
    plot_vel = np.zeros(shape=(int)(sim_end_time/time_step) + 1, dtype=np.float32)

    current_sim_time = 0
    dt = time_step

    # main loop
    for time_index in range(len(plot_time)):

        if finished(plot_vel, goal, time_index):
            if time_index != len(plot_time) - 1:
                (plot_time, plot_last_error, plot_goal, plot_vel) = clip_plots(time_index, plot_time, plot_last_error, plot_goal, plot_vel)
            break

        tm = (plot_time[time_index]+dt+(plot_time[time_index-1] if time_index > 0 else 0))
        plot_time[time_index] = tm

        # plot_time.append((plot_time[time_index]+dt) if time_index != -1 else dt)
        current_sim_time += dt

        # update objects
        car.update(dt)

        # plotting
        plot_last_error[time_index] = car.controller.last_error
        plot_goal[time_index] = goal
        plot_vel[time_index] = car.speed

        time_index += 1

    if current_sim_time <= sim_end_time:
        print("finished because output stabilized")
    else:
        print("finished because timeout")

    print("plotting...")
    plt.plot(plot_time, plot_vel, label="vel")
    plt.plot(plot_time, plot_goal, label="goal")
    plt.ylabel("velocity")
    plt.xlabel("time")
    plt.grid()
    plt.legend(loc="upper right")
    # plt.savefig("../fig/vel_time.png")
    plt.show()

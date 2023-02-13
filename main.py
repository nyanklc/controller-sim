import math
import time

from matplotlib import pyplot as plt

from car import Car
from viewer import Viewer

######################################################################
sim_end_time = 3.0

p = 0.002
i = 0.1
d = 0.00001

goal = 300.0

time_step = 0.001

finish_enabled = True
finish_error = 2
finish_derivative_error = 0.001

viewer_size = (640, 480)
######################################################################

def finished(value, goal):
    if (not finish_enabled):
        return False
    # basically checking if value is in the error range, AND if its derivative is close to zero
    if len(value) == 0:
        return False
    if math.fabs(value[len(value) - 1] - goal) < finish_error:
        diff = value[len(value) - 1] - value[len(value) - 2]
        if math.fabs(diff) < finish_derivative_error:
            return True
    return False

if __name__ == "__main__":
    car = Car(color=(255, 0, 255), x=200, y=100, yaw=math.pi/6)
    viewer = Viewer(viewer_size)

    pid_params = (p, i, d, goal) # assuming car starts with 0 velocity, otherwise also set last_measurement param
    car.setController('pid', pid_params)
    car.setSpeed(goal)

    print(f"INITIAL car speed: {car.speed}")

    # TODO: fix array lengths
    plot_time = []
    plot_last_error = []
    plot_goal = []
    plot_vel = []

    current_sim_time = 0
    while current_sim_time < sim_end_time and not finished(plot_vel, goal):
        dt = time_step
        if len(plot_time) == 0:
            time_index = -1
        else:
            time_index = len(plot_time) - 1
        print("TIME_INDEX: ", time_index)
        plot_time.append((plot_time[time_index]+dt) if time_index != -1 else dt)
        current_sim_time += dt

        print(f"BEFORE car speed: {car.speed}")
        car.update(dt)
        print(f"AFTER car speed: {car.speed}")

        # viewer
        viewer.draw(car)

        # plotting
        plot_last_error.append(car.controller.last_error)
        plot_goal.append(goal)
        plot_vel.append(car.speed)

        time.sleep(0.001)

    print("finished, plotting")
    # print("plot_time length:", len(plot_time))
    # print(plot_time)
    # print("plot_vel length:", len(plot_vel))
    # print(plot_vel)

    plt.plot(plot_time, plot_vel, label="vel")

    print("here")

    plt.plot(plot_time, plot_goal, label="goal")
    plt.ylabel("velocity")
    plt.xlabel("time")
    plt.grid("minor")
    plt.legend(loc="upper right")
    plt.show()

from car import Car
import time
import math
import matplotlib.pyplot as plt

######################################################################
sim_end_time = 10.0

p = 0.002
i = 0.1
d = 0.00001

goal = 50

time_step = 0.001

finish_error = 2
finish_derivative_error = 0.001
######################################################################

def finished(value, goal):
    # basically checking if value is in the error range, AND if its derivative is close to zero
    if math.fabs(value[len(value) - 1] - goal) < finish_error:
        diff = value[len(value) - 1] - value[len(value) - 2]
        if math.fabs(diff) < finish_derivative_error:
            return True
    return False
car = Car(10, 10)
pid_params = (p, i, d, goal) # assuming car starts with 0 velocity, otherwise also set last_measurement param
car.set_controller('pid', pid_params)

# TODO: fix array lengths
plot_time = [0.0, 0.0]
plot_last_error = []
plot_goal = [goal]
plot_vel = [0.0]

current_sim_time = 0
while current_sim_time < sim_end_time and not finished(plot_vel, goal):
    dt = time_step
    plot_time.append(dt)
    current_sim_time += dt

    car.update_vel(dt)

    # plotting
    plot_last_error.append(car.controller.last_error)
    plot_goal.append(goal)
    plot_vel.append(car.vel)

# TODO: this has bad performance
plot_time = [sum(plot_time[:i+1]) for i,j in enumerate(plot_time[:-1])]

plt.plot(plot_time, plot_vel, label="vel")
plt.plot(plot_time, plot_goal, label="goal")
plt.ylabel("velocity")
plt.xlabel("time")
plt.grid("minor")
plt.legend(loc="upper right")
plt.show()








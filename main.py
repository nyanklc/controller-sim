import math
import numpy as np
import pygame
import time

from car import Car, getDistance ,getAngle
from game_window import GameWindow

def perform_simulation(path):
    ####################################################
    meters_per_pixel = 0.005
    sim_step = 0.01  # seconds
    sample_frequency = 10  # Hz
    end_sim_distance = 0.1 # m

    goal_radius =  0.3 # m
    goal_index_range = 5

    master_linear_speed_limit = 0.2  # m/s
    master_angular_speed_limit = 1.7  # rad/s

    master_linear_control_multiplier = 1
    master_angular_control_multiplier = 8

    master_turn_limit_change_amount_linear = 0.1  # m/s
    master_turn_limit_change_amount_angular = 0.1 # rad/s
    ####################################################

    #path = [(x[0], 2*x[1]) for x in path2]

    # convert to pixel
    goal_radius /= meters_per_pixel
    master_linear_speed_limit /= meters_per_pixel
    master_turn_limit_change_amount_linear /= meters_per_pixel
    end_sim_distance /= meters_per_pixel

    master = Car((0,255,0),
                x=path[0][0],
                y=path[0][1],
                yaw=getAngle(path[0],path[1]),
                goal_rad=goal_radius,
                lin_max=master_linear_speed_limit,
                ang_max=master_angular_speed_limit,
                lin_mult=master_linear_control_multiplier,
                ang_mult=master_angular_control_multiplier,
                turn_limit_change_amount_linear=master_turn_limit_change_amount_linear,
                turn_limit_change_amount_angular=master_turn_limit_change_amount_angular,
                mpp=meters_per_pixel,
                camera_track=True,
                goal_index_range=goal_index_range)
    # linear speed controller
    p = 0.04
    i = 0.004
    d = 0.000001
    car_vel = 0
    pid_params = (p, i, d, car_vel)
    master.setController('pid', pid_params, 0.5, -0.5)
    # angular speed controller
    p = 0.4
    i = 0.04
    d = 0.00001
    car_angular_vel = 0
    pid_params = (p, i, d, car_angular_vel)
    master.setAngularController('pid', pid_params, 0.03, -0.03)

    window = GameWindow((640, 480))

    clock = pygame.time.Clock()
    curr_time = time.time()
    prev_time = curr_time

    tim = 0
    iteration_count = 0
    sample_count = 0
    time_arr = []
    lin_speed_arr = []
    ang_speed_arr = []
    pos_arr_x = []
    pos_arr_y = []
    while True:
        iteration_count += 1
        if master.goal_index == len(path) - 1:
            if getDistance((master.x, master.y), path[master.goal_index]) < end_sim_distance:
                break

        if master.goal_index != len(path)-1:
            master.get_goal(path)

        master.calculate_goal_yaw(path)

        master.update(sim_step, (path[master.goal_index][0], path[master.goal_index][1]), master.goal_yaw)

        # master.print_speeds()

        # record values
        tim += sim_step
        if tim > (sample_count / sample_frequency):
            sample_count += 1
            # print(f"tim: {tim}")
            # print(f"x: {master.x}, y: {master.y}")
            # print("#######################################")

            if tim != sim_step:
                time_arr.append(tim * 1000)  # append milliseconds
                lin_speed_arr.append(master.speed * meters_per_pixel)
                ang_speed_arr.append(master.angular_speed)
                pos_arr_x.append(master.x)
                pos_arr_y.append(master.y)

        window.draw([master], path)

    time_arr_np = np.array(time_arr)
    lin_speed_arr_np = np.array(lin_speed_arr)
    ang_speed_arr_np = np.array(ang_speed_arr)

    print(f"lin: {lin_speed_arr}")
    print(f"lin_length: {len(lin_speed_arr)}\n")
    print(f"ang: {ang_speed_arr}")
    print(f"ang_length: {len(ang_speed_arr)}\n")
    print(f"time: {time_arr}")
    print(f"time_length: {len(time_arr)}\n")
    print(f"expected completion duration: {tim} seconds")

    np.save("./time_arr.npy", time_arr_np)
    np.save("./lin_speed_arr.npy", lin_speed_arr_np)
    np.save("./ang_speed_arr.npy", ang_speed_arr_np)
    np.save("./pos_arr_x.npy", pos_arr_x)
    np.save("./pos_arr_y.npy", pos_arr_y)

    window.quit()

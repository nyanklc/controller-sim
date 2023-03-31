import math
import numpy as np
import pygame
import time

from car import Car, getDistance
from game_window import GameWindow

meters_per_pixel = 0.01
fps = 120
sim_step = 1 * meters_per_pixel

car = Car((0,255,0), x=200, y=100, yaw=0, socket_on=True)
# linear speed controller
p = 0.4
i = 0.04
d = 0.00001
car_vel = 0
pid_params = (p, i, d, car_vel)
car.setController('pid', pid_params)
# angular speed controller
p = 0.4
i = 0.04
d = 0.00001
car_angular_vel = 0
pid_params = (p, i, d, car_angular_vel)
car.setAngularController('pid', pid_params)

agent = Car((255,0,0), x=400, y=400, yaw=1)
# linear speed controller
p = 0.4
i = 0.04
d = 0.00001
car_vel = 0
pid_params = (p, i, d, car_vel)
agent.setController('pid', pid_params)
# angular speed controller
p = 0.4
i = 0.04
d = 0.00001
car_angular_vel = 0
pid_params = (p, i, d, car_angular_vel)
agent.setAngularController('pid', pid_params)

window = GameWindow((640, 480))

clock = pygame.time.Clock()
curr_time = time.time()
prev_time = curr_time
while True:
    clock.tick(fps)

    curr_time = time.time()
    # print(f"fps: {1 / (curr_time - prev_time)}")
    prev_time = time.time()

    car.update(sim_step)
    agent.update(sim_step, (car.x - 200, car.y), car.yaw)

    window.set_info_text("distance: %d px" % (getDistance((car.x, car.y), (agent.x, agent.y))), (0, 0, 0))
    window.draw([car, agent])
    
    events = window.get_events()
    for event in events:
        if event.type == pygame.QUIT:
            window.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            # car
            if event.key == pygame.K_UP:
                car.setSpeed(car.getSpeedGoal() + 10)
            if event.key == pygame.K_DOWN:
                car.setSpeed(car.getSpeedGoal() - 10)
            if event.key == pygame.K_RIGHT:
                car.setAngularSpeed(car.getAngularSpeedGoal() + 0.5)
            if event.key == pygame.K_LEFT:
                car.setAngularSpeed(car.getAngularSpeedGoal() - 0.5)
            # agent
            if event.key == pygame.K_w:
                agent.setSpeed(agent.getSpeedGoal() + 10)
            if event.key == pygame.K_s:
                agent.setSpeed(agent.getSpeedGoal() - 10)
            if event.key == pygame.K_d:
                agent.setAngularSpeed(agent.getAngularSpeedGoal() + 0.5)
            if event.key == pygame.K_a:
                agent.setAngularSpeed(agent.getAngularSpeedGoal() - 0.5)

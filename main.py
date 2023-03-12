import math
import numpy as np
import pygame
import time

from car import Car
from game_window import GameWindow

meters_per_pixel = 0.01
fps = 60
sim_step = 1 * meters_per_pixel

car = Car((0,255,0), x=200, y=100, yaw=math.pi/6)
p = 0.4
i = 0.04
d = 0.00001
car_vel = 0
pid_params = (p, i, d, car_vel)
car.setController('pid', pid_params)

window = GameWindow((640, 480))

clock = pygame.time.Clock()
curr_time = time.time()
prev_time = curr_time
while True:
    clock.tick(fps)

    curr_time = time.time()
    print(f"fps: {1 / (curr_time - prev_time)}")
    prev_time = time.time()

    car.update(sim_step)
    window.set_info_text("car speed: %.2f m/s (%.2f px/s)" % (car.getSpeed() * meters_per_pixel, car.getSpeed()), (0, 0, 0))
    window.draw([car])
    events = window.get_events()
    for event in events:
        if event.type == pygame.QUIT:
            window.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car.setSpeed(car.getSpeedGoal() + 10)
            if event.key == pygame.K_DOWN:
                car.setSpeed(car.getSpeedGoal() - 10)
            if event.key == pygame.K_LEFT:
                pass
            if event.key == pygame.K_RIGHT:
                pass
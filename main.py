import math
import numpy as np
import pygame

from car import Car
from game_window import GameWindow

# TODO: making time step smaller results in unstable controller behavior
sim_step = 0.01

car = Car((0,255,0), x=200, y=100, yaw=math.pi/6)
p = 0.2
i = 0.1
d = 0.0001
car_vel = 0
pid_params = (p, i, d, car_vel)
car.setController('pid', pid_params)

window = GameWindow((640, 480))

while True:
    print(f"car speed: {car.getSpeed()}")
    car.update(sim_step)
    window.draw(car)
    events = window.get_events()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("up")
                car.setSpeed(car.getSpeedGoal() + 1)
                print(car.getSpeedGoal())
            if event.key == pygame.K_DOWN:
                print("down")
                car.setSpeed(car.getSpeedGoal() - 1)
                print(car.getSpeedGoal())
            if event.key == pygame.K_LEFT:
                print("left")
                pass
            if event.key == pygame.K_RIGHT:
                print("right")
                pass
import math
import numpy as np
import pygame
import time

from car import Car, getDistance
from game_window import GameWindow

def calculateYaw(x1, x2, y1, y2):
    return math.atan2(y1 - y2, x1 - x2)


meters_per_pixel = 0.01
fps = 120
sim_step = 1 * meters_per_pixel

car = Car((0,255,0), x=320, y=240, yaw=0, socket_on=True)

prev_x = car.x
prev_y = car.y

window = GameWindow((640, 480))

clock = pygame.time.Clock()
curr_time = time.time()
prev_time = curr_time
while True:
    clock.tick(fps)

    curr_time = time.time()
    # print(f"fps: {1 / (curr_time - prev_time)}")
    prev_time = time.time()

    window.set_info_text("car speed: %.2f m/s (%.2f px/s)" % (car.getSpeed() * meters_per_pixel, car.getSpeed()), (0, 0, 0))
    window.draw([car])

    curr_x, curr_y = car.receive()
    # curr_x *= 3
    # curr_y *= 3

    curr_x += 640/2
    curr_y += 480/2

    dyaw = calculateYaw(curr_x, prev_x, curr_y, prev_y)
    dx = curr_x - prev_x
    dy = curr_y - prev_y
    car.updateRemote(dx, dy, dyaw)
    prev_x = curr_x
    prev_y = curr_y

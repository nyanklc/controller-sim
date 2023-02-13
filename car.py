import math

from object import Object
from pid import PIDController

class Car(Object):
    def __init__(self, color:tuple, size:float=50, x:float=0, y:float=0, yaw:float=0, initial_speed:float=0):
        Object.__init__(self, shape_type="rectangle", color=color, radius=math.sqrt(2) * size / 2, x=x, y=y, yaw=yaw)
        self.speed:float = initial_speed

    def update(self, dt):
        dx = math.cos(self.yaw) * self.speed * dt
        dy = math.sin(self.yaw) * self.speed * dt
        Object.update(self, dx, dy)
        self.speed += self.controller.update(self.speed, dt)

    def setSpeed(self, value):
        self.controller.setGoal(value)

    def setController(self, method, params):
        if method == 'pid':
            p = params[0]
            i = params[1]
            d = params[2]
            set_value = params[3]
            # TODO: read other params as well
            self.controller = PIDController(p, i, d, set_value)

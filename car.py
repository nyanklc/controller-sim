import math

from object import Object
from pid import PIDController

class Car(Object):
    def __init__(self, color:tuple, size:float=50, x:float=0, y:float=0, yaw:float=0, initial_speed:float=0):
        Object.__init__(self, shape_type="rectangle", color=color, radius=math.sqrt(2) * size / 2, x=x, y=y, yaw=yaw)
        self.speed:float = initial_speed
        self.angular_speed = 0

    def update(self, dt):
        dx = math.cos(self.yaw) * self.speed * dt
        dy = math.sin(self.yaw) * self.speed * dt
        dyaw = self.angular_speed * dt
        Object.update(self, dx, dy, dyaw)
        self.speed += self.controller.update(self.speed, dt)
        self.angular_speed += self.angular_controller.update(self.angular_speed, dt)

    def setSpeed(self, value):
        self.controller.setGoal(value)

    def setAngularSpeed(self, value):
        self.angular_controller.setGoal(value)

    def getSpeed(self):
        return self.speed
    
    def getAngularSpeed(self):
        return self.angular_speed

    def getSpeedGoal(self):
        return self.controller.getGoal()
    
    def getAngularSpeedGoal(self):
        return self.angular_controller.getGoal()

    def setController(self, method, params):
        if method == 'pid':
            p = params[0]
            i = params[1]
            d = params[2]
            set_value = params[3]
            # TODO: read other params as well
            self.controller = PIDController(p, i, d, set_value)

    def setAngularController(self, method, params):
        if method == 'pid':
            p = params[0]
            i = params[1]
            d = params[2]
            set_value = params[3]
            # TODO: read other params as well
            self.angular_controller = PIDController(p, i, d, set_value)
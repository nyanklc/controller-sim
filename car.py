import math
import socket
import struct
import time

from object import Object
from pid import PIDController

def getAngle(base, head):
    return math.atan2(head[1]-base[1], head[0]-base[0])

def getAngularDifference(th1, th2):
    if th1 == th2:
        return 0

    diff = math.atan2(math.cos(th1) * math.sin(th2) - math.cos(th2) * math.sin(th1),
                      math.sin(th1) * math.sin(th2) + math.cos(th1) * math.cos(th2))
    while diff > math.pi:
        diff -= 2*math.pi
    while diff < -math.pi:
        diff += 2*math.pi

    return diff

def getDistance(point1, point2):
    return math.hypot(point2[1]-point1[1], point2[0]-point1[0])

class Car(Object):
    def __init__(self, color:tuple, size:float=50, x:float=0, y:float=0, yaw:float=0, initial_speed:float=0, socket_on=False):
        Object.__init__(self, shape_type="rectangle", color=color, radius=math.sqrt(2) * size / 2, x=x, y=y, yaw=yaw)
        self.speed:float = initial_speed
        self.angular_speed = 0
        self.has_orientation = True

        if socket_on:
          self.socket_on = socket_on
          self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.sock.connect(("192.168.4.1", 333))
          self.last_send_time = time.time()
          self.socket_output_stream = self.sock.makefile('w')

    def updateAutomatic(self, pos, yaw, dt):
        yaw_should_be = getAngle((self.x, self.y), pos)
        self.angular_controller.setGoal(getAngularDifference(self.yaw, yaw_should_be) * 5)
        self.controller.setGoal(getDistance((self.x, self.y), pos) * 5)
        self.speed += self.controller.update(self.speed, dt)
        self.angular_speed += self.angular_controller.update(self.angular_speed, dt)

    """ automatic mode if goal is provided """
    def update(self, dt, goal_position=None, goal_yaw=None):
        dx = math.cos(self.yaw) * self.speed * dt
        dy = math.sin(self.yaw) * self.speed * dt
        dyaw = self.angular_speed * dt
        Object.update(self, dx, dy, dyaw)

        if goal_position is not None and goal_yaw is not None:
            self.updateAutomatic(goal_position, goal_yaw, dt)
            return
        
        self.speed += self.controller.update(self.speed, dt)
        self.angular_speed += self.angular_controller.update(self.angular_speed, dt)

        if (self.socket_on):
          meters_per_pixel = 0.01
          data_str = '{:.2f} {:.2f}a'.format(self.speed * meters_per_pixel, self.angular_speed)
          # if (time.time() - self.last_send_time) < 0.2:
          #   return
          print("sending: ", data_str)
          self.socket_output_stream.write(data_str)
          self.socket_output_stream.flush()
          self.last_send_time = time.time()

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

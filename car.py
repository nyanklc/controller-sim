from pid import PIDController

class Car:
    def __init__(self, width, height, initial_vel=0):
        self.w = width
        self.h = height
        self.vel = initial_vel

    def update_vel(self, dt):
        self.vel += self.controller.update(self.vel, dt)

    def set_controller(self, method, params):
        if method == 'pid':
            p = params[0]
            i = params[1]
            d = params[2]
            set_value = params[3]
            # TODO: read other params as well
            self.controller = PIDController(p, i, d, set_value)

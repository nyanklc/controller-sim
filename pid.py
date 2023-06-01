class PIDController:
    def __init__(self, p, i, d, set_value, last_error=0, last_measurement=0, lim_min=-30, lim_max=30):
        self.Kp = p
        self.Ki = i
        self.Kd = d

        self.lim_min = lim_min
        self.lim_max = lim_max # ?

        self.goal = set_value

        self.last_error = last_error
        self.last_measurement = last_measurement

        self.integrator = 0
        self.differentiator = 0

        self.out : float

    def update(self, measurement, dt) -> float:
        error = self.goal - measurement

        # proportional term
        proportional = self.Kp * error

        # filtered integral term
        integral = self.integrator + 0.5 * self.Ki * dt * (error - self.last_error)

        # clamp integral term (anti-windup via dynamic integrator clamping)
        lim_min_int : float
        lim_max_int : float
        if self.lim_max > proportional:
            lim_max_int = self.lim_max - proportional
        else:
            lim_max_int = 0.0
        if self.lim_min < proportional:
            lim_min_int = self.lim_min - proportional
        else:
            lim_min_int = 0.0

        if integral > lim_max_int:
            integral = lim_max_int
        elif integral < lim_min_int:
            integral = lim_min_int

        # derivative term (bandlimited differentiator) (derivative on measurement to prevent kick)
        # TODO: tau?
        self.tau = 0.02
        derivative = -(2.0 * self.Kd * (measurement - self.last_measurement) + (2.0 * self.tau - dt) * self.differentiator) / (2.0 * self.tau + dt)

        self.out = proportional + integral + derivative

        # limit the output
        if self.out > self.lim_max:
            self.out = self.lim_max
        elif self.out < self.lim_min:
            self.out = self.lim_min

        # memory
        self.last_error = error
        self.last_measurement = measurement
        self.integrator = integral
        self.differentiator = derivative

        return self.out

    def setGoal(self, newint):
        self.goal = newint

    def getGoal(self):
        return self.goal

import math

class Sim:
    def __init__(
        self,
        duration,
        time_step,
        controller_class,
        controller_params,
        end_tolerance,
        end_derivative_tolerance
        ):
        self.sim_duration = duration
        self.time_step = time_step
        self.controller_class = controller_class
        self.controller_class_params = controller_params
        self.sim_end_tolerance = end_tolerance
        self.sim_end_derivative_tolerance = end_derivative_tolerance

    def isFinished(self, value, goal):
        # basically checking if value is in the error range, AND if its derivative is close to zero
        if math.fabs(value[len(value) - 1] - goal) < self.sim_end_tolerance:
            diff = value[len(value) - 1] - value[len(value) - 2]
            if math.fabs(diff) < finish_derivative_error:
                return True
        return False
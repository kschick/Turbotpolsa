from rlbot.agents.base_agent import SimpleControllerState


class Maneuver:

    def __init__(self, car):
        self.car: Car = car
        self.controls: SimpleControllerState = SimpleControllerState()
        self.finished: bool = False

    def step(self, dt: float):
        pass
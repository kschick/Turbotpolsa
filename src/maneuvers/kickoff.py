import math
from rlbot.agents.base_agent import SimpleControllerState

from maneuvers.maneuver import Maneuver
from maneuvers.drive import Drive
from util.vec import Vec3


class Kickoff(Maneuver):
    def __init__(self, car, info):
        super().__init__(car)
        self.info = info
        self.drive = Drive(car, ball.pos)

    def step(self, dt) -> SimpleControllerState:
        self.controls = SimpleControllerState()
        ball = self.info.ball
        self.controls = self.drive.step(dt)

        if ball.pos.x != 0.0 and ball.pos.y != 0.0:
            self.finished = True

        return self.controls

import math
from rlbot.agents.base_agent import SimpleControllerState

from routines.routine import Routine
from states.drive import Drive
from util.vec import Vec3


class Kickoff(Routine):
    def __init__(self):
        super().__init__()
        self.drive = Drive()

    def exec(self, bot) -> SimpleControllerState:
        self.controls = SimpleControllerState()
        ball = bot.info.ball
        my_car = bot.info.my_car
        self.controls = self.drive.go_towards_point(bot, ball.pos)

        if ball.pos.x != 0.0 and ball.pos.y != 0.0:
            self.done = True

        return self.controls

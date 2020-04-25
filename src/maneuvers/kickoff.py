import math
from rlbot.agents.base_agent import SimpleControllerState

from maneuvers.maneuver import Maneuver
from maneuvers.drive import Drive
from util.vec import Vec3


class Kickoff(Maneuver):
    def __init__(self, bot):
        super().__init__(bot)
        ball = bot.info.ball
        self.drive = Drive(bot, ball.pos)

    def step(self, dt) -> SimpleControllerState:
        self.controls = SimpleControllerState()
        ball = self.bot.info.ball
        self.controls = self.drive.step(dt)

        if ball.pos.x != 0.0 and ball.pos.y != 0.0:
            self.finished = True

        return self.controls

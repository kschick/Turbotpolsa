from rlbot.agents.base_agent import SimpleControllerState


class Maneuver:

    def __init__(self, bot):
        self.bot  = bot
        self.controls: SimpleControllerState = SimpleControllerState()
        self.finished: bool = False

    def step(self, dt: float):
        pass
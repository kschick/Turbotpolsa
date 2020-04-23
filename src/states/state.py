from rlbot.agents.base_agent import SimpleControllerState


class State:
    def exec(self, bot) -> SimpleControllerState:
        raise NotImplementedError

    def reset(self):
        pass

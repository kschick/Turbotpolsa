from rlbot.agents.base_agent import SimpleControllerState

from routines.routine import Routine


class Flip(Routine):
    def __init__(self, bot,
                 target=None,
                 boost=False,
                 t_first_jump=0.10,
                 t_first_wait=0.00,
                 t_aim=0.08,
                 t_second_jump=0.28,
                 t_second_wait=0.14):
        super().__init__()

        self._start_time = bot.info.time
        self._almost_finished = False

        self._t_first_unjump = t_first_jump
        self._t_aim = self._t_first_unjump + t_first_wait
        self._t_second_jump = self._t_aim + t_aim
        self._t_second_unjump = self._t_second_jump + t_second_jump
        self._t_finishing = self._t_second_unjump + t_second_wait  # After this, fix orientation until lands on ground

        self._t_steady_again = 0.25  # Time on ground before steady and ready again

    def exec(self, bot) -> SimpleControllerState:
        ct = bot.info.time - self._start_time
        controls = SimpleControllerState()
        controls.throttle = 1
        car = bot.info.my_car

        corner_debug = "ct: {}\n".format(ct)
        corner_debug += "_start_time: {}\n".format(self._start_time)
        corner_debug += "_t_finishing: {}\n".format(type(self._t_finishing))
        bot.renderer.draw_string_2d(10, 200, 1, 1,
                            corner_debug, bot.renderer.white())

        if ct >= self._t_finishing:
            self._almost_finished = True
            if car.on_ground:
                self.done = True
            # else:
                # bot.maneuver = RecoveryManeuver(bot)
                # self.done = True
            return controls
        elif ct >= self._t_second_unjump:
            # Stop pressing jump and rotate and wait for flip is done
            pass
        elif ct >= 0.08:
            if ct >= self._t_second_jump:
                controls.jump = 1

            controls.roll = 0
            controls.pitch = -1
            controls.yaw = 0
        # Stop pressing jump
        elif ct >= self._t_first_unjump:
            pass

        # First jump
        else:
            controls.jump = 1

        return controls

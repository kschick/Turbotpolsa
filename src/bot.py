import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import xy, Vec3, norm, dot
from util.info import GameInfo

from states.drive import Drive
from routines.kickoff import Kickoff

RENDER = True


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.do_rendering = RENDER
        self.info = None
        self.state = None
        self.routine = None
        self.doing_kickoff = False

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.info = GameInfo(self.index, self.team)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Read packet
        if not self.info.field_info_loaded:
            self.info.read_field_info(self.get_field_info())
            if not self.info.field_info_loaded:
                return SimpleControllerState()
        self.info.read_packet(packet)

        draw_debug(self.renderer, self.info.my_car, self.info.ball, self)

        self.controller_state = self.make_decision()

        self.renderer.end_rendering()

        return self.controller_state

    def make_decision(self) -> SimpleControllerState:

        car = self.info.my_car
        ball = self.info.ball

        # Check kickoff
        if self.info.is_kickoff and not self.doing_kickoff:
            self.routine = Kickoff()
            self.doing_kickoff = True

        if self.routine is not None:
            if self.routine.done:
                self.doing_kickoff = False
                self.routine = None
            else:
                return self.routine.exec(self)

        

        # # if right_side_of_ball:
        #     self.state = Drive()
        # else:
            # self.state = Drive()

        if type(self.state) != Drive:
                self.state = Drive()
                
        return self.state.exec(self)


def draw_debug(renderer, car, ball, bot):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    # renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    # renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    corner_debug = "Car velocity: {}\n".format(norm(car.vel))
    corner_debug += "Car pos x: {}\n".format(round(car.pos.x))
    corner_debug += "Car pos y: {}\n".format(round(car.pos.y))
    corner_debug += "Car boost: {}\n".format(car.boost)
    corner_debug += "State: {}\n".format(type(bot.state))
    corner_debug += "Routine: {}\n".format(type(bot.routine))
    corner_display_y = 900 - (corner_debug.count('\n') * 20)
    renderer.draw_string_2d(10, corner_display_y, 1, 1,
                            corner_debug, renderer.white())

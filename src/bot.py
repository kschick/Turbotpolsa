import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import xy, Vec3, norm, dot
from util.info import GameInfo

from maneuvers.drive import Drive
from maneuvers.kickoff import Kickoff

RENDER = True


class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.do_rendering = RENDER
        self.info = None
        self.maneuver = None
        self.doing_kickoff = False
        self.time = 0
        self.prev_time = 0

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controls = SimpleControllerState()
        self.info = GameInfo(self.index, self.team)

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Read packet
        if not self.info.field_info_loaded:
            self.info.read_field_info(self.get_field_info())
            if not self.info.field_info_loaded:
                return SimpleControllerState()
        self.info.read_packet(packet)

        self.time = self.info.time
        dt = self.time - self.prev_time
        self.prev_time = self.time

        draw_debug(self.renderer, self.info.my_car, self.info.ball, self)

         # choose maneuver
        if self.maneuver is None:
            self.maneuver = self.choose_maneuver()

        if self.maneuver is not None:
            self.maneuver.step(dt)
            self.controls = self.maneuver.controls

            if self.maneuver.finished:
                self.maneuver = None

        self.renderer.end_rendering()

        return self.controls

    def choose_maneuver(self) -> SimpleControllerState:

        car = self.info.my_car
        ball = self.info.ball

        # Check kickoff
        if self.info.is_kickoff and not self.doing_kickoff:
            self.doing_kickoff = True
            return Kickoff(self)

        return Drive(self, ball.pos)


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
    corner_debug += "Maneuver: {}\n".format(type(bot.maneuver))

    corner_display_y = 900 - (corner_debug.count('\n') * 20)
    renderer.draw_string_2d(10, corner_display_y, 1, 1,
                            corner_debug, renderer.white())

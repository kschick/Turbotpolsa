import math

from rlbot.agents.base_agent import SimpleControllerState

from states.state import State
from routines.flip import Flip
from util.vec import xy, Vec3, norm, dot
from util.rlmath import clip



class Drive(State):
    def __init__(self):
        self.controls = SimpleControllerState()
        self.last_flip_end_time = 0
        self.flip = None

    def exec(self, bot) -> SimpleControllerState:
        car = bot.info.my_car
        ball = bot.info.ball

        car_to_ball = ball.pos - car.pos
        dist = norm(car_to_ball)


        ball_to_enemy_goal = bot.info.enemy_goal - ball.pos
        own_goal_to_ball = ball.pos - bot.info.own_goal

        offence = ball.pos.y * bot.info.team_sign < 0
        dot_enemy = dot(car_to_ball, ball_to_enemy_goal)
        dot_own = dot(car_to_ball, own_goal_to_ball)
        right_side_of_ball = dot_enemy > 0 if offence else dot_own > 0

        if right_side_of_ball:
            self.go_towards_point(bot, ball.pos)
        else:
            self.go_towards_point(bot, bot.info.own_goal_field)    
        return self.controls

    def go_towards_point(self, bot, point) -> SimpleControllerState:

        car = bot.info.my_car
        car_to_point = point - car.pos
        dist = norm(car_to_point)
        point_local = dot(point - car.pos, car.rot)

        # Angle to point in local xy plane and other stuff
        angle = math.atan2(point_local.y, point_local.x)
        # dist = norm(point_local)


        # Flip is done
        if self.flip is not None and self.flip.done:
            self.flip = None
            self.last_flip_end_time = bot.info.time
        # Continue flip
        elif self.flip is not None:
            return self.flip.exec(bot)

        time_since_last_flip = bot.info.time - self.last_flip_end_time
        if dist > 2000 and abs(angle) <= 0.02 and time_since_last_flip > 3:
            self.flip = Flip(bot)
            return self.flip.exec(bot)

        # Boost?
        if norm(car.vel) < 2200 and abs(angle) <= 0.02:
            self.controls.boost = True

        self.controls.steer = clip(angle + (2.5 * angle) ** 3, -1.0, 1.0)
        self.controls.throttle = 1.0

        corner_debug = "steer: {}\n".format(self.controls.steer)
        bot.renderer.draw_string_2d(10, 200, 1, 1,
                            corner_debug, bot.renderer.white())

        return self.controls

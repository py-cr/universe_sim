# -*- coding:utf-8 -*-
# title           :
# description     :
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Body, Sun, Earth, Moon
from objs import Satellite, Satellite2
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import calc_run
from bodies.body import AU
from simulators.calc_simulator import CalcSimulator, CalcContext

bodies = [
    Earth(init_position=[0, 0, 0], texture="earth_hd.jpg",
          init_velocity=[0, 0, 0], size_scale=0.5e1),  # 地球放大 5 倍，距离保持不变
    Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
         init_velocity=[-1.054152222, 0, 0], size_scale=1e1)  # 月球放大 10 倍，距离保持不变
]


def evolve_next(context: CalcContext):
    return context.evolve_count < 200


def after_evolve(dt, context: CalcContext):
    moon: Body = context.bodies[1]
    print(moon.acceleration_value(), moon.velocity_value())


CalcSimulator.on_after_evolve_subscription(after_evolve)

calc_run(bodies, SECONDS_PER_HOUR, evolve_next=evolve_next)
